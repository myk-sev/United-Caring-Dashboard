import csv
from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from shelters.models import ShelterInputModel
from whiteflag.models import WhiteFlag


class ReportsViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="reports", password="secret123")
        ShelterInputModel.objects.create(shelter="mens", regular=5, respite=1, guests=0, hospital=0, jail=0, no_show=0, barred=0, hold=0)
        ShelterInputModel.objects.create(shelter="womens", regular=7, respite=1, guests=0, hospital=0, jail=0, no_show=0, barred=0, hold=0)
        self.current_whiteflag = WhiteFlag.objects.create(men=1, women=2, children=3, non_binary=0)
        self.old_whiteflag = WhiteFlag.objects.create(men=4, women=3, children=2, non_binary=1)
        WhiteFlag.objects.filter(pk=self.old_whiteflag.pk).update(
            submitted_at=timezone.now() - timedelta(days=10)
        )

    def test_reports_filter_by_shelter(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("reports"), {"shelter": "mens"})
        self.assertEqual(response.status_code, 200)
        shelter_data = list(response.context["shelter_data"])
        self.assertEqual(len(shelter_data), 1)
        self.assertEqual(shelter_data[0].shelter, "mens")
        self.assertEqual(list(response.context["whiteflag_data"]), [])

    def test_reports_can_filter_whiteflag_records(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("reports"), {"shelter": "whiteflag"})
        self.assertEqual(list(response.context["shelter_data"]), [])
        self.assertEqual(len(response.context["whiteflag_data"]), 2)

    def test_export_includes_csv_header(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("Type,Date,Shelter", response.content.decode("utf-8"))

    def test_default_export_link_has_no_none_parameters(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("reports"))
        self.assertContains(response, 'href="/reports/export/"')
        self.assertNotContains(response, "None")

    def test_invalid_export_date_returns_bad_request(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("export"), {"start": "not-a-date"})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Start date must be a valid date", status_code=400)

    def test_whiteflag_export_excludes_shelter_rows(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("export"), {"shelter": "whiteflag"})
        rows = list(csv.reader(StringIO(response.content.decode("utf-8"))))
        self.assertEqual({row[0] for row in rows[1:]}, {"WhiteFlag"})

    def test_date_filter_applies_to_whiteflag_reports_and_exports(self):
        self.client.login(username="reports", password="secret123")
        start = (timezone.localdate() - timedelta(days=1)).isoformat()

        response = self.client.get(reverse("reports"), {"start": start})
        self.assertEqual(
            list(response.context["whiteflag_data"]),
            [self.current_whiteflag],
        )

        response = self.client.get(reverse("export"), {"start": start})
        rows = list(csv.reader(StringIO(response.content.decode("utf-8"))))
        record_numbers = {row[11] for row in rows if row and row[0] == "WhiteFlag"}
        self.assertEqual(record_numbers, {str(self.current_whiteflag.pk)})

    def test_import_creates_records_from_csv(self):
        self.client.login(username="reports", password="secret123")
        csv_content = "Type,Date,Shelter,Regular Beds,Respite Beds,Guests On Pass,Hospital,Jail,No Show,Barred,Hold,Record Number,Men,Women,Children,Non Binary,Total,Submitted At\n"
        csv_content += "Shelter,2026-01-02,diversion,3,0,0,0,0,0,0,0,,,,,,,\n"
        csv_content += "WhiteFlag,,,,,,,,,,,99,1,1,1,1,4,2026-01-02 00:00:00\n"
        upload = SimpleUploadedFile("import.csv", csv_content.encode("utf-8"), content_type="text/csv")

        response = self.client.post(reverse("import"), {"file": upload})
        self.assertEqual(response.status_code, 302)
        shelter = ShelterInputModel.objects.get(shelter="diversion", regular=3)
        self.assertEqual(shelter.date.isoformat(), "2026-01-02")
        whiteflag = WhiteFlag.objects.get(record_number=99, total=4)
        self.assertEqual(timezone.localdate(whiteflag.submitted_at).isoformat(), "2026-01-02")

    def test_invalid_import_is_atomic_and_reports_the_row(self):
        self.client.login(username="reports", password="secret123")
        csv_content = ",".join([
            "Type", "Date", "Shelter", "Regular Beds", "Respite Beds",
            "Guests On Pass", "Hospital", "Jail", "No Show", "Barred", "Hold",
            "Record Number", "Men", "Women", "Children", "Non Binary", "Total",
            "Submitted At",
        ]) + "\n"
        csv_content += "Shelter,2026-01-02,diversion,3,0,0,0,0,0,0,0,,,,,,,\n"
        csv_content += "Shelter,2026-01-03,invalid,3,0,0,0,0,0,0,0,,,,,,,\n"
        upload = SimpleUploadedFile("import.csv", csv_content.encode("utf-8"), content_type="text/csv")

        response = self.client.post(reverse("import"), {"file": upload}, follow=True)
        self.assertContains(response, "Import failed: Row 3: select a valid shelter")
        self.assertFalse(ShelterInputModel.objects.filter(shelter="diversion").exists())

    def test_import_rejects_non_csv_files_without_crashing(self):
        self.client.login(username="reports", password="secret123")
        upload = SimpleUploadedFile("import.txt", b"not csv", content_type="text/plain")
        response = self.client.post(reverse("import"), {"file": upload}, follow=True)
        self.assertContains(response, "Import failed: Select a CSV file")
