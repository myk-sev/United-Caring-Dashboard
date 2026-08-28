from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.test import TestCase
from django.urls import reverse

from .models import AdminSettings


class AdminPanelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="adminuser", password="secret123")
        self.admin_password = "integration-admin"
        AdminSettings.objects.update_or_create(
            defaults={"admin_password": make_password(self.admin_password)}
        )

    def test_admin_login_requires_user_login(self):
        response = self.client.get(reverse("admin_login"))
        self.assertEqual(response.status_code, 302)

    def test_admin_password_sets_session_and_redirects(self):
        self.client.login(username="adminuser", password="secret123")
        response = self.client.post(reverse("admin_login"), {"admin_password": self.admin_password})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("admin_page_one"))
        self.assertTrue(self.client.session.get("is_admin"))

    def test_admin_can_change_an_application_password(self):
        self.client.login(username="adminuser", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()

        response = self.client.post(reverse("admin_page_two"), {
            "change_login_password": "1",
            "target_username": self.user.username,
            "login_new_password1": "updated-password",
            "login_new_password2": "updated-password",
        })

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password("updated-password"))

    def test_admin_can_change_the_admin_panel_password(self):
        self.client.login(username="adminuser", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()

        response = self.client.post(reverse("admin_page_two"), {
            "change_password": "1",
            "old_password": self.admin_password,
            "new_password1": "updated-admin",
            "new_password2": "updated-admin",
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_password(
            "updated-admin",
            AdminSettings.objects.get().admin_password,
        ))

    def test_admin_logout_clears_admin_session(self):
        self.client.login(username="adminuser", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()
        response = self.client.get(reverse("admin_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("mainscreen"))
        self.assertNotIn("is_admin", self.client.session)
