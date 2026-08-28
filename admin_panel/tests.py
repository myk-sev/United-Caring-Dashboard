from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from shelters.models import ShelterInputModel


@override_settings(ADMIN_PANEL_PASSWORD="integration-admin")
class AdminPanelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="adminuser", password="secret123")
        self.admin_password = "integration-admin"

    def enter_admin(self):
        self.client.login(username="adminuser", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()

    def test_admin_login_requires_user_login(self):
        response = self.client.get(reverse("admin_login"))
        self.assertEqual(response.status_code, 302)

    def test_admin_password_sets_session_and_redirects(self):
        self.client.login(username="adminuser", password="secret123")
        response = self.client.post(reverse("admin_login"), {"admin_password": self.admin_password})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("admin_page_one"))
        self.assertTrue(self.client.session.get("is_admin"))

    def test_incorrect_admin_password_is_rejected(self):
        self.client.login(username="adminuser", password="secret123")
        response = self.client.post(reverse("admin_login"), {
            "admin_password": "incorrect",
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("is_admin", self.client.session)

    def test_admin_can_change_an_application_password(self):
        self.enter_admin()

        response = self.client.post(reverse("admin_page_two"), {
            "change_login_password": "1",
            "target_username": self.user.username,
            "login_new_password1": "updated-password",
            "login_new_password2": "updated-password",
        })

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password("updated-password"))

    def test_admin_panel_password_is_not_editable_in_the_app(self):
        self.enter_admin()

        response = self.client.get(reverse("admin_page_two"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="change_password"')

    def test_record_search_handles_invalid_or_missing_input(self):
        self.enter_admin()

        response = self.client.post(reverse("admin_page_two"), {
            "search_records": "1",
            "search_input_shelter": "mens",
            "search_input_id": "not-a-number",
        }, follow=True)
        self.assertContains(response, "Record number must be numeric.")

        response = self.client.post(reverse("admin_page_two"), {
            "search_records": "1",
            "search_input_shelter": "mens",
            "search_input_id": "999",
        }, follow=True)
        self.assertContains(response, "No matching record was found.")

        response = self.client.post(reverse("admin_page_two"), {
            "search_records": "1",
            "search_input_shelter": "mens",
            "search_input_date": "not-a-date",
        }, follow=True)
        self.assertContains(response, "Enter a valid record date.")

    def test_shelter_edit_preserves_record_and_changes_date(self):
        self.enter_admin()
        record = ShelterInputModel.objects.create(
            shelter="mens", regular=1, respite=1, guests=1, hospital=1,
            jail=1, no_show=1, barred=1, hold=1,
        )

        response = self.client.post(reverse("admin_page_two"), {
            "alter_records": "1",
            "record_type": "shelter",
            "old_id": record.id,
            "date": "2026-05-01",
            "shelter": "mens",
            "regular": 2,
            "respite": 1,
            "guests": 1,
            "hospital": 1,
            "jail": 1,
            "no_show": 1,
            "barred": 1,
            "hold": 1,
        })

        record.refresh_from_db()
        self.assertRedirects(response, reverse("admin_page_two"))
        self.assertEqual(record.regular, 2)
        self.assertEqual(record.date.isoformat(), "2026-05-01")
        self.assertEqual(ShelterInputModel.objects.count(), 1)

    def test_invalid_shelter_edit_does_not_delete_record(self):
        self.enter_admin()
        record = ShelterInputModel.objects.create(
            shelter="mens", regular=1, respite=1, guests=1, hospital=1,
            jail=1, no_show=1, barred=1, hold=1,
        )

        response = self.client.post(reverse("admin_page_two"), {
            "alter_records": "1",
            "record_type": "shelter",
            "old_id": record.id,
            "date": "2026-05-01",
            "shelter": "mens",
            "regular": "",
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ShelterInputModel.objects.filter(pk=record.pk).exists())

    def test_save_controls_are_hidden_until_a_record_is_selected(self):
        self.enter_admin()
        response = self.client.get(reverse("admin_page_two"))
        self.assertNotContains(response, 'name="alter_records"')

    def test_admin_logout_clears_admin_session(self):
        self.client.login(username="adminuser", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()
        response = self.client.get(reverse("admin_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("mainscreen"))
        self.assertNotIn("is_admin", self.client.session)
