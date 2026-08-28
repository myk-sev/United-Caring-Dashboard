from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="dash", password="secret123")

    def test_home_requires_authentication(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_home_redirects_to_the_live_dashboard(self):
        self.client.login(username="dash", password="secret123")
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, reverse("admin_page_one"), fetch_redirect_response=False)
