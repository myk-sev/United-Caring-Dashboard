from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from reports.models import ShiftReport
from shelters.models import Shelter, ShelterInputModel
from whiteflag.models import WhiteFlag


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
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save(update_fields=["is_staff", "is_superuser"])
        self.enter_admin()

        response = self.client.post(reverse("admin_page_two"), {
            "change_login_password": "1",
            "target_username": self.user.username,
            "login_new_password1": "Stronger-Login-Password-934!",
            "login_new_password2": "Stronger-Login-Password-934!",
        })

        self.user.refresh_from_db()
        self.assertRedirects(response, reverse("admin_page_two"))
        self.assertTrue(self.user.check_password("Stronger-Login-Password-934!"))

    def test_non_privileged_admin_cannot_change_application_passwords(self):
        self.enter_admin()
        target = get_user_model().objects.create_user(username="target", password="original-pass-934")
        response = self.client.post(reverse("admin_page_two"), {
            "change_login_password": "1",
            "target_username": target.username,
            "login_new_password1": "Stronger-Login-Password-934!",
            "login_new_password2": "Stronger-Login-Password-934!",
        }, follow=True)
        target.refresh_from_db()
        self.assertTrue(target.check_password("original-pass-934"))
        self.assertContains(response, "do not have permission to change login passwords")

    def test_password_change_uses_django_password_validation(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save(update_fields=["is_staff", "is_superuser"])
        self.enter_admin()
        response = self.client.post(reverse("admin_page_two"), {
            "change_login_password": "1",
            "target_username": self.user.username,
            "login_new_password1": "password",
            "login_new_password2": "password",
        }, follow=True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("secret123"))
        self.assertContains(response, "This password is too common")

    def test_admin_panel_password_is_not_editable_in_the_app(self):
        self.enter_admin()

        response = self.client.get(reverse("admin_page_two"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="change_password"')
        self.assertNotContains(response, 'name="change_login_password"')

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

    def test_admin_can_persist_capacity_settings(self):
        self.enter_admin()
        page = self.client.get(reverse("admin_page_two"))
        self.assertContains(page, 'name="change_capacities"')
        self.assertContains(page, "UPDATE CAPACITIES")

        response = self.client.post(reverse("admin_page_two"), {
            "change_capacities": "1",
            "mens_regular_capacity": 51,
            "mens_respite_capacity": 8,
            "womens_regular_capacity": 23,
            "womens_respite_capacity": 5,
            "diversion_regular_capacity": 6,
            "whiteflag_capacity": 81,
        })

        self.assertRedirects(response, reverse("admin_page_two"))
        self.assertEqual(Shelter.objects.get(name="mens").total_beds, 51)
        self.assertEqual(Shelter.objects.get(name="womens").respite_beds, 5)
        self.assertEqual(Shelter.objects.get(name="whiteflag").total_beds, 81)

    def test_admin_dashboard_uses_current_records_and_capacities(self):
        self.enter_admin()
        ShelterInputModel.objects.create(
            shelter="womens", regular=10, respite=2, guests=0, hospital=0,
            jail=0, no_show=0, barred=0, hold=0,
        )
        ShelterInputModel.objects.create(
            shelter="diversion", regular=3, respite=0, guests=0, hospital=0,
            jail=0, no_show=0, barred=0, hold=0,
        )

        response = self.client.get(reverse("admin_page_one"))

        self.assertEqual(response.context["womens_regular_available"], 12)
        self.assertEqual(response.context["womens_respite_available"], 2)
        self.assertEqual(response.context["diversion_regular_available"], 2)
        self.assertEqual(response.context["womens_utilization"], 46)

    def test_admin_logout_clears_admin_session(self):
        self.client.login(username="adminuser", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()
        response = self.client.get(reverse("admin_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("mainscreen"))
        self.assertNotIn("is_admin", self.client.session)

    def test_database_tool_requires_a_superuser(self):
        self.enter_admin()
        response = self.client.get(reverse("admin_page_three"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A superuser account is required")
        self.assertNotContains(response, 'name="clear_database"')

        response = self.client.post(reverse("admin_page_three"), {
            "clear_database": "1",
            "confirmation": "DELETE",
        })
        self.assertEqual(response.status_code, 403)

    def test_database_tool_requires_admin_session(self):
        self.client.login(username="adminuser", password="secret123")
        response = self.client.get(reverse("admin_page_three"))
        self.assertRedirects(response, reverse("admin_login"))

    def test_database_tool_requires_exact_delete_confirmation(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save(update_fields=["is_staff", "is_superuser"])
        self.enter_admin()
        record = ShelterInputModel.objects.create(
            shelter="mens", regular=1, respite=0, guests=0, hospital=0,
            jail=0, no_show=0, barred=0, hold=0,
        )

        response = self.client.post(reverse("admin_page_three"), {
            "clear_database": "1",
            "confirmation": "delete",
        }, follow=True)

        self.assertTrue(ShelterInputModel.objects.filter(pk=record.pk).exists())
        self.assertContains(response, "Enter DELETE in all caps to continue")

    def test_database_tool_clears_only_operational_records(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save(update_fields=["is_staff", "is_superuser"])
        self.enter_admin()
        capacity = Shelter.objects.create(name="mens", total_beds=50, respite_beds=7)
        ShelterInputModel.objects.create(
            shelter="mens", regular=1, respite=0, guests=0, hospital=0,
            jail=0, no_show=0, barred=0, hold=0,
        )
        WhiteFlag.objects.create(men=1)
        ShiftReport.objects.create(
            shelter="mens", shift="close", beds_used=1, beds_available=49,
        )

        response = self.client.post(reverse("admin_page_three"), {
            "clear_database": "1",
            "confirmation": "DELETE",
        }, follow=True)

        self.assertFalse(ShelterInputModel.objects.exists())
        self.assertFalse(WhiteFlag.objects.exists())
        self.assertFalse(ShiftReport.objects.exists())
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())
        self.assertTrue(Shelter.objects.filter(pk=capacity.pk).exists())
        self.assertContains(response, "Accounts and capacity settings were preserved")
