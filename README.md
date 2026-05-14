<p align="center">
  <img src="docs/united-caring-dashboard-logo.svg" alt="United Caring Dashboard logo" width="140">
</p>

<h1 align="center">United Caring Dashboard</h1>

<p align="center">
  A Django dashboard for shelter operations, shift reporting, white-flag workflows, and administrative review.
</p>

## Live Demo

The deployed application is available at:

[https://united-caring-dashboard.onrender.com/](https://united-caring-dashboard.onrender.com/)

## Overview

United Caring Dashboard brings common shelter management workflows into one shared interface for staff and administrators. The application supports shelter selection, shift submissions, white-flag condition tracking, report review, and custom administrative pages.

The project is organized as a multi-app Django system:

- `mainscreen`: Main landing workflow and shelter selection.
- `accounts`: Login, logout, and account-related views.
- `dashboard`: Central dashboard views and metrics.
- `shelters`: Shelter data, forms, and shift submission flows.
- `whiteflag`: White-flag status pages and related forms.
- `reports`: Report-oriented views and data models.
- `admin_panel`: Custom admin login and administrative pages.

## Tech Stack

- Python
- Django
- HTML templates
- Bootstrap
- SQLite for local development
- Render for deployment

## Local Development

1. Clone the repository and move into the project folder.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```


4. Run database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open the local site:

   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Project Structure

```text
United-Caring-Dashboard/
+-- accounts/
+-- admin_panel/
+-- dashboard/
+-- docs/
+-- mainscreen/
+-- reports/
+-- shelters/
+-- shelter_system/
+-- templates/
+-- whiteflag/
+-- manage.py
+-- README.md
+-- requirements.txt
```

## Key Routes

- `/`: Main screen and shelter selection.
- `/login/`: User login.
- `/shelters/`: Shelter shift submission flow.
- `/white-flag/`: White-flag reporting workflow.
- `/reports/`: Reports view.
- `/admin-panel/`: Custom admin panel login.

## Admin Panel Password

The admin panel password is stored as a hashed value in the database — it is never stored in plain text in code or environment variables.

After running migrations (step 4), a default password is seeded. Contact the project administrator for login credentials.

**This password should be changed immediately after any fresh deployment or database reset** using the password change feature inside the admin panel.

If the production database is ever deleted or recreated, migrations will reseed the default password and it must be changed again. Never delete the production database without first noting the current admin password or coordinating with the site administrator.

## Notes

This repository is configured for local SQLite development by default. Production deployment settings should be managed through environment variables and the hosting platform.
