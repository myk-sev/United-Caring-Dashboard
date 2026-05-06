# United Caring Dashboard

![United Caring Dashboard logo](./docs/assets/united-caring-dashboard.png)

The **United Caring Dashboard** is a Django web app for shelter operations teams to collect daily intake/occupancy data and view summarized dashboard/reporting pages in one place.

## Try it live

👉 **Live app:** https://united-caring-dashboard.onrender.com/

## What the app does

- Authenticated staff log in to access the application.
- A central main screen routes users to shelter data entry workflows.
- Shelter teams submit occupancy and related information through forms.
- Dashboard and report pages provide a shared operational view.
- A White Flag workflow captures high-demand/capacity-period data.
- An admin panel path is available from the main screen through an administrator password flow.

## Application flow

1. User signs in at `/login/`.
2. User lands on the main screen (`/mainscreen/`).
3. User chooses a shelter workflow and submits shelter data at `/shelters/`.
4. User can access:
   - Dashboard: `/dashboard/`
   - Reports: `/reports/`
   - White Flag: `/white-flag/`

## Project structure

- `shelter_system/` – project settings and global URL routing.
- `accounts/` – authentication views (login/logout).
- `mainscreen/` – home routing screen for staff/admin path.
- `shelters/` – shelter intake/occupancy form workflow.
- `dashboard/` – dashboard page.
- `reports/` – reports page.
- `whiteflag/` – white flag form and edit workflow.
- `admin_panel/` – administrator pages.

## Local development

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment variables

Create a `.env` file in the repo root with values for:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL` (optional)

### 3) Run migrations and start server

```bash
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

---

If you are looking for a quick product walkthrough, start with the live deployment above and follow the flow from login → main screen → shelters/dashboard/reports/white flag.
