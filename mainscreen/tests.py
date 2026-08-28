from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class MainScreenTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="main", password="secret123")

    def test_mainscreen_requires_authentication(self):
        response = self.client.get(reverse("mainscreen"))
        self.assertEqual(response.status_code, 302)

    def test_shelter_selection_routes_to_the_selected_shelter(self):
        self.client.login(username="main", password="secret123")
        response = self.client.get(reverse("mainscreen"), {"shelter": "mens"})
        self.assertRedirects(
            response,
            f'{reverse("shelters")}?shelter=mens',
            fetch_redirect_response=False,
        )

    def test_whiteflag_selection_routes_to_whiteflag(self):
        self.client.login(username="main", password="secret123")
        response = self.client.get(reverse("mainscreen"), {"shelter": "whiteflag"})
        self.assertRedirects(response, reverse("whiteflag"), fetch_redirect_response=False)

    def test_legacy_mainscreen_url_redirects_to_main_screen(self):
        self.client.login(username="main", password="secret123")
        response = self.client.get("/mainscreen/")
        self.assertRedirects(response, reverse("mainscreen"), status_code=301)
