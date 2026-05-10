from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class MainScreenTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="main", password="secret123")

    def test_mainscreen_requires_authentication(self):
        response = self.client.get(reverse("mainscreen"))
        self.assertEqual(response.status_code, 302)

    def test_shelter_selection_routes_to_shelters(self):
        self.client.login(username="main", password="secret123")
        response = self.client.post(reverse("mainscreen"), {"shelter_go": "1", "shelter_select": "mens"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("shelters"))
