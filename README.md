# Munib and Co — Chartered Accountant Web App

A full Django site for Munib and Co, built from your brochure: public marketing pages, client
self-registration, role-based dashboards with 3D Plotly analytics, a document exchange system,
and client↔admin messaging with password reset.

## What's included

- **Public site**: Home, Services (all 7 services from the brochure), Why Choose Us, Contact
- **Auth**: Register, login (username or email), profile edit, change password, full password reset
- **Client dashboard**: total spend, pending/completed services, 3D scatter plot of service
  history, status donut chart, service history table
- **Admin dashboard**: firm-wide stats, 3D bar chart of revenue by service, 3D surface chart of
  monthly revenue trend, status donut, recent records table
- **Service Records**: admin logs billable engagements per client (feeds the 3D charts)
- **Documents**: clients upload files to the firm; admin sends files back to clients; both can
  download/delete their own uploads
- **Messaging**: real-time-feel chat thread between each client and the admin, with file
  attachments and an unread badge in the navbar

## 1. Setup (Windows PowerShell)

```powershell
cd munib_co
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Environment file

Copy `.env.example` to `.env`. The defaults work out of the box with SQLite and local file
storage — you don't need to fill anything in to run it locally.

```powershell
Copy-Item .env.example .env
```

## 3. Run migrations

```powershell
python manage.py migrate
```

## 4. Create your admin (staff) account

```powershell
python manage.py createsuperuser
```

After creating it, log into `/admin/` once and set that user's **role** field to `admin` (or set
`is_staff=True`, which also counts as admin in this app). Client accounts created through the
public "Get Started" registration form are automatically role `client`.

## 5. Run the server

```powershell
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Password reset

By default, `EMAIL_BACKEND` is set to the console backend — reset links print straight to your
terminal instead of sending real email, so you can test the whole flow with zero setup. When
you're ready to send real emails, switch `EMAIL_BACKEND` in `.env` to the SMTP backend and fill
in `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` (a Gmail App Password works well).

## Adding service records (so the 3D charts have data)

Log in as admin → **Service Records** → **+ New Record**. Add a few entries with different
service types, months, and amounts for a client, and the 3D bar/surface charts on the admin
dashboard and the 3D scatter on that client's dashboard will populate automatically.

## Deploying (Vercel + Neon + Cloudinary — your usual stack)

1. Push this project to GitHub.
2. Create a Neon Postgres database, and in Vercel's environment variables set:
   `USE_POSTGRES=True`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`
3. Create a Cloudinary account and set `USE_CLOUDINARY=True`, `CLOUDINARY_CLOUD_NAME`,
   `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` (Vercel's filesystem is ephemeral, so this is
   required for uploaded documents/chat attachments to persist).
4. Set `SECRET_KEY`, `DEBUG=False`, and `CSRF_TRUSTED_ORIGINS` to your Vercel domain.
5. Import the project into Vercel — `vercel.json` and `build_files.sh` are already configured.

## Notes on the 3D charts

The three chart types (3D bar, 3D surface, 3D scatter, plus a styled donut) all live in
`dashboard/analytics.py` using Plotly's `graph_objects`. They render as embedded HTML/JS divs
directly in the dashboard templates — no extra API calls needed. If you want a different chart
type (e.g. a true 3D pie via `Mesh3d`, or a bubble chart), that file is the only place you need
to touch.
