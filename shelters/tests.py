from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from shelters.models import Shelter, ShelterInputModel


class SheltersViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="shelter", password="secret123")

    def test_get_sets_capacity_from_selected_shelter(self):
        self.client.login(username="shelter", password="secret123")
        response = self.client.get(f"{reverse('shelters')}?shelter=womens")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["capacity"], 22)

        Shelter.objects.create(name="womens", total_beds=30, respite_beds=6)
        response = self.client.get(f"{reverse('shelters')}?shelter=womens")
        self.assertEqual(response.context["capacity"], 30)
        self.assertEqual(response.context["respite_capacity"], 6)

    def test_get_without_a_shelter_returns_to_selection(self):
        self.client.login(username="shelter", password="secret123")
        response = self.client.get(reverse("shelters"))
        self.assertRedirects(response, reverse("mainscreen"))

    def test_post_creates_record_and_redirects(self):
        self.client.login(username="shelter", password="secret123")
        payload = {
            "shelter": "mens",
            "regular": 10,
            "respite": 1,
            "guests": 2,
            "hospital": 0,
            "jail": 0,
            "no_show": 0,
            "barred": 0,
            "hold": 0,
        }
        response = self.client.post(reverse("shelters"), payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShelterInputModel.objects.count(), 1)
        self.assertIn("shelter=mens", response.url)

        page = self.client.get(response.url)
        self.assertContains(page, "Re-Submit")
        self.assertContains(page, "Last submitted:")

    def test_invalid_submission_keeps_values_and_shows_errors(self):
        self.client.login(username="shelter", password="secret123")
        payload = {
            "shelter": "mens",
            "regular": 51,
            "respite": 1,
            "guests": -2,
            "hospital": 0,
            "jail": 0,
            "no_show": 0,
            "barred": 0,
            "hold": 0,
        }
        response = self.client.post(reverse("shelters"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Occupied beds cannot exceed capacity.")
        self.assertContains(response, "Enter zero or a positive number.")
        self.assertEqual(response.context["form"]["regular"].value(), "51")
        self.assertFalse(ShelterInputModel.objects.exists())

    def test_resubmit_updates_the_same_record(self):
        self.client.login(username="shelter", password="secret123")
        record = ShelterInputModel.objects.create(
            shelter="mens", regular=1, respite=1, guests=0, hospital=0,
            jail=0, no_show=0, barred=0, hold=0,
        )
        payload = {
            "record_id": record.id,
            "shelter": "mens",
            "regular": 2,
            "respite": 1,
            "guests": 0,
            "hospital": 0,
            "jail": 0,
            "no_show": 0,
            "barred": 0,
            "hold": 0,
        }
        response = self.client.post(reverse("shelters"), payload)
        record.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(record.regular, 2)
        self.assertEqual(ShelterInputModel.objects.count(), 1)

    def test_new_record_link_opens_a_blank_form(self):
        self.client.login(username="shelter", password="secret123")
        ShelterInputModel.objects.create(
            shelter="mens", regular=10, respite=1, guests=0, hospital=0,
            jail=0, no_show=0, barred=0, hold=0,
        )
        response = self.client.get(f"{reverse('shelters')}?shelter=mens&new=1")
        self.assertIsNone(response.context["record"])
        self.assertEqual(response.context["regular_open"], 50)
        self.assertContains(response, 'id="regular_occupied"')

    def test_diversion_page_guards_missing_respite_inputs(self):
        self.client.login(username="shelter", password="secret123")
        response = self.client.get(f"{reverse('shelters')}?shelter=diversion")
        self.assertContains(response, "if (respite_occupied && respite_open)", html=False)
