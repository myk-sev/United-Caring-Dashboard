from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from shelters.models import ShelterInputModel
from whiteflag.models import WhiteFlag


class ReportsViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="reports", password="secret123")
        ShelterInputModel.objects.create(shelter="mens", regular=5, respite=1, guests=0, hospital=0, jail=0, no_show=0, barred=0, hold=0)
        ShelterInputModel.objects.create(shelter="womens", regular=7, respite=1, guests=0, hospital=0, jail=0, no_show=0, barred=0, hold=0)
        WhiteFlag.objects.create(men=1, women=2, children=3, non_binary=0)

    def test_reports_filter_by_shelter(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("reports"), {"shelter": "mens"})
        self.assertEqual(response.status_code, 200)
        shelter_data = list(response.context["shelter_data"])
        self.assertEqual(len(shelter_data), 1)
        self.assertEqual(shelter_data[0].shelter, "mens")

    def test_export_includes_csv_header(self):
        self.client.login(username="reports", password="secret123")
        response = self.client.get(reverse("export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("Type,Date,Shelter", response.content.decode("utf-8"))

    def test_import_creates_records_from_csv(self):
        self.client.login(username="reports", password="secret123")
        csv_content = "Type,Date,Shelter,Regular Beds,Respite Beds,Guests On Pass,Hospital,Jail,No Show,Barred,Hold,Record Number,Men,Women,Children,Non Binary,Total,Submitted At\n"
        csv_content += "Shelter,2026-01-02,diversion,3,0,0,0,0,0,0,0,,,,,,,\n"
        csv_content += "WhiteFlag,,,,,,,,,,,99,1,1,1,1,4,2026-01-02 00:00:00\n"
        upload = SimpleUploadedFile("import.csv", csv_content.encode("utf-8"), content_type="text/csv")

        response = self.client.post(reverse("import"), {"file": upload})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ShelterInputModel.objects.filter(shelter="diversion", regular=3).exists())
        self.assertTrue(WhiteFlag.objects.filter(record_number=99, total=4).exists())
