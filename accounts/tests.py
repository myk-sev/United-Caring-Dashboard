from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class AccountsViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tester", password="secret123")

    def test_login_success_redirects_home(self):
        response = self.client.post(reverse("login"), {"username": "tester", "password": "secret123"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_login_invalid_credentials_shows_error(self):
        response = self.client.post(reverse("login"), {"username": "tester", "password": "wrong"}, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertTrue(any("Invalid username or password." in str(m) for m in messages))

    def test_logout_clears_session_and_redirects(self):
        self.client.login(username="tester", password="secret123")
        session = self.client.session
        session["is_admin"] = True
        session.save()

        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")
        self.assertNotIn("_auth_user_id", self.client.session)