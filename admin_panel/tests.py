from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminPanelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="adminuser", password="secret123")

    def test_admin_login_requires_user_login(self):
        response = self.client.get(reverse("admin_login"))
        self.assertEqual(response.status_code, 302)

    def test_admin_password_sets_session_and_redirects(self):
        self.client.login(username="adminuser", password="secret123")
        response = self.client.post(reverse("admin_login"), {"admin_password": settings.ADMIN_PANEL_PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("admin_page_one"))
        self.assertTrue(self.client.session.get("is_admin"))

    def test_admin_logout_clears_admin_session(self):
        self.client.login(username="adminuser", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()
        response = self.client.get(reverse("admin_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("mainscreen"))
        self.assertNotIn("is_admin", self.client.session)
