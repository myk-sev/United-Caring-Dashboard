from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from shelters.models import Shelter
from whiteflag.models import WhiteFlag


class WhiteFlagTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="white", password="secret123")

    def test_create_whiteflag_record_and_redirect_to_edit(self):
        self.client.login(username="white", password="secret123")
        response = self.client.post(reverse("whiteflag_submission"), {
            "men": 2,
            "women": 1,
            "children": 1,
            "non_binary": 0,
        })
        self.assertEqual(response.status_code, 302)
        record = WhiteFlag.objects.get()
        self.assertEqual(record.total, 4)
        self.assertEqual(response.url, reverse("whiteflag_edit", kwargs={"pk": record.pk}))

    def test_edit_whiteflag_record_updates_counts(self):
        self.client.login(username="white", password="secret123")
        record = WhiteFlag.objects.create(men=1, women=1, children=0, non_binary=0)
        response = self.client.post(reverse("whiteflag_submission"), {
            "record_number": record.pk,
            "men": 3,
            "women": 1,
            "children": 1,
            "non_binary": 1,
        })
        self.assertEqual(response.status_code, 302)
        record.refresh_from_db()
        self.assertEqual(record.total, 6)

    def test_landing_page_handles_an_empty_database(self):
        self.client.login(username="white", password="secret123")
        response = self.client.get(reverse("whiteflag"))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_uses_persisted_capacity(self):
        self.client.login(username="white", password="secret123")
        Shelter.objects.create(name="whiteflag", total_beds=90, respite_beds=0)
        response = self.client.get(reverse("whiteflag"))
        self.assertEqual(response.context["capacity"], 90)

    def test_landing_page_opens_todays_record(self):
        self.client.login(username="white", password="secret123")
        record = WhiteFlag.objects.create(men=1)
        response = self.client.get(reverse("whiteflag"))
        self.assertRedirects(
            response,
            reverse("whiteflag_edit", kwargs={"pk": record.pk}),
        )

    def test_invalid_submission_returns_form_errors(self):
        self.client.login(username="white", password="secret123")
        response = self.client.post(reverse("whiteflag_submission"), {
            "men": -1,
            "women": 0,
            "children": 0,
            "non_binary": 0,
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(WhiteFlag.objects.exists())

    def test_submission_cannot_exceed_capacity(self):
        self.client.login(username="white", password="secret123")
        response = self.client.post(reverse("whiteflag_submission"), {
            "men": 81,
            "women": 0,
            "children": 0,
            "non_binary": 0,
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "cannot exceed the White Flag capacity of 80", status_code=400)
        self.assertFalse(WhiteFlag.objects.exists())

    def test_second_submission_updates_todays_record(self):
        self.client.login(username="white", password="secret123")
        record = WhiteFlag.objects.create(men=1)
        response = self.client.post(reverse("whiteflag_submission"), {
            "men": 2,
            "women": 1,
            "children": 0,
            "non_binary": 0,
        })
        self.assertRedirects(response, reverse("whiteflag_edit", kwargs={"pk": record.pk}))
        self.assertEqual(WhiteFlag.objects.count(), 1)
        record.refresh_from_db()
        self.assertEqual(record.total, 3)

    def test_edit_page_shows_remaining_availability_without_new_record_link(self):
        self.client.login(username="white", password="secret123")
        record = WhiteFlag.objects.create(men=50, women=20)
        response = self.client.get(reverse("whiteflag_edit", kwargs={"pk": record.pk}))
        self.assertEqual(response.context["availability"], 10)
        self.assertNotContains(response, "New Record")
