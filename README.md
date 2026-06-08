# 🗂️ Dashboardz

A full-stack **Dashboard Web Application** built with Python and Django that enables users to create their own custom data tables, manage records with full CRUD operations, and visualise their data through interactive Chart.js charts — all behind a secure, multi-method authentication system.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [Apps & Modules](#apps--modules)
  - [Authentication App](#authentication-app)
  - [Records App](#records-app)
- [URL Reference](#url-reference)
- [Features In Detail](#features-in-detail)
  - [Authentication & Security](#authentication--security)
  - [CRUD Operations](#crud-operations)
  - [Data Visualisation with Chart.js](#data-visualisation-with-chartjs)
    - [How the Data Flows to the Chart](#how-the-data-flows-to-the-chart)
    - [Chart Types](#chart-types)
    - [Dropdown-Driven Dynamic Switching](#dropdown-driven-dynamic-switching)
    - [Chart.js Configuration Highlights](#chartjs-configuration-highlights)
  - [Export](#export)
  - [UX Enhancements](#ux-enhancements)
- [Templates & UI](#templates--ui)
- [Configuration & Environment Variables](#configuration--environment-variables)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)

---

## Project Overview

Dashboardz lets each authenticated user create their own named data tables with custom field labels, add rows of data (a numeric value, a category, a date, and a description), and see those records reflected live in **Chart.js** visualisations — switchable between bar, line, pie, and doughnut charts via a dropdown with no page reload. The app is fully multi-user — every table, record, and category is scoped to the logged-in user.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 5.1 |
| Frontend | Django Template Language, HTML, Tailwind CSS, JavaScript |
| Database | MySQL |
| Visualisation | Chart.js |
| Authentication | Django auth + Django Allauth (Google OAuth) |
| Email | SMTP (TLS, port 587) |
| Environment | `python-dotenv` for credential management |
| Other | Django Messages Framework, Pagination |

---

## Project Structure

```
dashboardz/
├── dashboardz/                   # Django project config
│   ├── settings.py               # All project settings, DB, email, OAuth
│   ├── urls.py                   # Root URL conf (includes app-level urls)
│   ├── static/
│   │   ├── img/                  # Logo assets
│   │   └── js/
│   │       └── confirmDelete.js  # Delete confirmation modal JS
│   ├── asgi.py
│   └── wsgi.py
├── authentication/               # Authentication Django app
│   ├── views.py                  # All auth views (Login, Register, Verify, Reset...)
│   ├── urls.py                   # Auth-level URL routing
│   ├── utils.py                  # Token generator for email verification
│   ├── adapters.py               # Custom allauth adapter (Google OAuth redirect)
│   ├── admin.py
│   └── migrations/
├── records/                      # Core records/dashboard Django app
│   ├── views.py                  # CRUD views (main, Add, Edit, Delete)
│   ├── models.py                 # All data models (managed=False, MySQL-first)
│   ├── urls.py                   # Records-level URL routing
│   ├── admin.py
│   └── migrations/
├── templates/
│   ├── base.html                 # Main layout (sidebar, nav, messages)
│   ├── base_auth.html            # Auth-only layout
│   ├── main.html                 # Landing page for unauthenticated users
│   ├── messages.html             # Reusable Django messages partial
│   ├── partials/
│   │   ├── sidebar.html          # Sidebar with user's table list
│   │   └── modal.html            # Reusable delete confirmation modal
│   ├── authentication/
│   │   ├── login.html
│   │   ├── register.html         # With real-time JS validation
│   │   ├── reset-password.html
│   │   ├── set-new-password.html
│   │   └── terms-of-service.html
│   ├── records/
│   │   ├── records.html          # Main dashboard (table + Chart.js charts)
│   │   ├── add-table.html        # Create new table + optional first row
│   │   ├── add-table-data.html   # Add new row to existing table
│   │   ├── edit-table-data.html  # Edit existing row
│   │   └── privacy-policy.html
│   └── errors/
│       └── error404.html         # Custom 404 page
├── manage.py
└── .env                          # Not committed — see Environment Variables section
```

---

## Database Design

The database schema was designed as an ER diagram first, then modelled in **MySQL Workbench** and forward-engineered to create the tables. Django models are set to `managed = False` since the schema is owned by MySQL Workbench, not Django migrations.

### `records_name`
The top-level table representing a user's named data table.

| Column | Type | Notes |
|---|---|---|
| `id` | BIGINT PK | Auto increment |
| `name` | VARCHAR(45) | Unique per application |
| `owner` | VARCHAR (FK → `auth_user.username`) | Scopes table to a user |

### `field_names`
Stores the custom column labels the user sets when creating a table. Each table has exactly one `FieldNames` row.

| Column | Type | Notes |
|---|---|---|
| `id` | BIGINT PK | |
| `field_1` | VARCHAR(45) | Label for the numeric field |
| `field_2` | VARCHAR(45) | Label for the category field |
| `field_3` | VARCHAR(45) | Label for the date field |
| `records_name_id` | FK → `records_name` | |
| `owner` | FK → `auth_user.username` | |

### `field_2_names`
Stores the category options (dropdown values) available for `field_2` within a given table.

| Column | Type | Notes |
|---|---|---|
| `id` | BIGINT PK | |
| `name` | VARCHAR(45) | Category label |
| `records_name_id` | FK → `records_name` | |
| `owner` | FK → `auth_user.username` | |

> Unique constraint: `(records_name_id, name)`

### `field_values`
Stores the actual data rows entered by the user.

| Column | Type | Notes |
|---|---|---|
| `id` | BIGINT PK | |
| `field_1` | DECIMAL(20,3) | Numeric value (max 999,999) |
| `field_2_id` | FK → `field_2_names` | Category (dropdown selection) |
| `field_3` | DATE | Date field |
| `description` | TEXT | Free-text description |
| `owner` | FK → `auth_user.username` | |
| `records_name_id` | FK → `records_name` | |

> Default ordering: `-field_3` (newest date first)

**Entity relationships:**

```
auth_user
  └── owns → RecordsName (one user, many tables)
               ├── has one → FieldNames  (column labels)
               ├── has many → Field2Names (category options)
               └── has many → FieldValues (data rows)
```

---

## Apps & Modules

### Authentication App

**`authentication/views.py`** contains all auth logic as class-based views:

| Class / Function | Route | Description |
|---|---|---|
| `LoginView` | `GET/POST /authentication/` | Credential-based login with Django `authenticate()` |
| `RegistrationView` | `GET/POST /authentication/register` | Creates user, sends verification email via SMTP thread |
| `VerificationView` | `GET /authentication/activate/<uidb64>/<token>` | Activates account from email link |
| `UsernameValidationView` | `POST /authentication/validate-username` | Real-time AJAX username check (alphanumeric, unique) |
| `EmailValidationView` | `POST /authentication/validate-email` | Real-time AJAX email check (valid format, unique) |
| `RequestPasswordResetEmail` | `GET/POST /authentication/reset-password` | Sends password reset link to registered email |
| `CompletePasswordReset` | `GET/POST /authentication/reset-password-link/<uidb64>/<token>` | Validates token and sets new password |
| `LogoutView` | `POST /authentication/logout` | Logs out and redirects to login |
| `tos` | `GET /authentication/terms-of-service` | Renders Terms of Service page |

**`authentication/utils.py`** — Custom token generator extending Django's `PasswordResetTokenGenerator` for email verification tokens.

**`authentication/adapters.py`** — Custom `allauth` adapter (`MyAccountAdapter`) to handle Google OAuth redirect behaviour.

**`EmailThread`** — A `threading.Thread` subclass that sends emails asynchronously so registration/password-reset responses are not blocked by SMTP latency.

---

### Records App

**`records/views.py`** contains the core dashboard and CRUD logic:

| View | Route | Description |
|---|---|---|
| `main` (function) | `GET /` or `GET /<int:id>/` | Main dashboard — shows table data + charts. Auto-selects first table if no `id` passed. Returns landing page if unauthenticated. |
| `AddTableView` | `GET/POST /add-table` | Creates a new table (RecordsName + FieldNames). Optionally inserts the first data row in the same form. |
| `AddTableDataView` | `GET/POST /add-table-data/<int:id>` | Adds a new `FieldValues` row to an existing table. Creates new `Field2Names` category on the fly if "Other" is selected. |
| `EditTableDataView` | `GET/POST /edit-table-data/<int:id>` | Edits an existing `FieldValues` row. |
| `DeleteTableDataView` | `POST /delete-table-data/<int:id>` | Deletes a `FieldValues` row. Rejects non-POST with an error message. |
| `error404` | — | Custom 404 handler registered via `handler404`. |
| `privacy_policy` | `GET /privacy-policy` | Static privacy policy page. |

All CRUD views use `LoginRequiredMixin` (or `@never_cache` for function views) to enforce authentication and prevent back-button access to stale cached pages.

---

## URL Reference

### Project-level (`dashboardz/urls.py`)

| Pattern | Includes / Points to |
|---|---|
| `/admin/` | Django admin |
| `/` | `records.urls` |
| `/authentication/` | `authentication.urls` |
| `/accounts/login/` | Redirect to Google OAuth |
| `/accounts/` | `allauth.urls` |

### Records app

| Method | URL | View | Name |
|---|---|---|---|
| GET | `/` | `main` | `records` |
| GET | `/<int:id>/` | `main` | `records` |
| GET | `/privacy-policy` | `privacy_policy` | `privacy-policy` |
| GET/POST | `/add-table` | `AddTableView` | `add-table` |
| GET/POST | `/add-table-data/<int:id>` | `AddTableDataView` | `add-table-data` |
| GET/POST | `/edit-table-data/<int:id>` | `EditTableDataView` | `edit-table-data` |
| POST | `/delete-table-data/<int:id>` | `DeleteTableDataView` | `delete-table-data` |

### Authentication app

| Method | URL | View | Name |
|---|---|---|---|
| GET/POST | `/authentication/` | `LoginView` | `login` |
| GET/POST | `/authentication/register` | `RegistrationView` | `register` |
| POST | `/authentication/logout` | `LogoutView` | `logout` |
| GET | `/authentication/activate/<uidb64>/<token>` | `VerificationView` | `activate` |
| POST | `/authentication/validate-username` | `UsernameValidationView` | `validate-username` |
| POST | `/authentication/validate-email` | `EmailValidationView` | `validate-email` |
| GET/POST | `/authentication/reset-password` | `RequestPasswordResetEmail` | `reset-password` |
| GET/POST | `/authentication/reset-password-link/<uidb64>/<token>` | `CompletePasswordReset` | `reset-password-link` |
| GET | `/authentication/terms-of-service` | `tos` | `tos` |

---

## Features In Detail

### Authentication & Security

- **Standard login/logout** with Django's built-in `authenticate()` and `login()`.
- **Registration** with email verification — the account is created with `is_active=False` and activated only when the user clicks the emailed link.
- **Google OAuth** via `django-allauth` — users can sign in with Google in addition to username/password.
- **Password reset** via tokenised email link using `PasswordResetTokenGenerator`.
- **`@never_cache`** decorator on all authenticated views to prevent sensitive pages from being served from browser cache after logout.
- **Login attempt limit** — `ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5` via allauth.

### CRUD Operations

- **Create table** — User defines a table name and three custom field labels (a numeric label, a category label, and a date label). Optionally inserts the first data row in the same step.
- **Add data** — User selects from existing `Field2Names` category options via dropdown, or types a new category ("Other") which is created automatically with `get_or_create`.
- **Edit data** — Pre-populates form with existing row values; updates in-place on save.
- **Delete data** — POST-only; confirmed via a JavaScript modal before submission. Rejects GET requests with an error message.
- **Field 1 validation** — Numeric field enforced as `Decimal`, capped at 999,999. Validation errors returned to the same page with the user's previous inputs preserved.

### Data Visualisation with Chart.js

Charts are rendered directly inside `records/records.html` using **Chart.js** (loaded via CDN). All chart logic lives in the template's `<script>` block — no separate JS file is needed for the charts because the data is injected by Django's template engine before the page is served.

#### How the Data Flows to the Chart

The `main` view passes the current table's `FieldValues` queryset to the template via context. Inside the template, Django's template language loops over those values and serialises them into JavaScript arrays that Chart.js reads:

```
Django view (records/views.py)
  └── passes FieldValues queryset → template context
        ↓
records/records.html (DTL loops)
  └── builds JS arrays: labels[], numerics[], dates[], categories[]
        ↓
Chart.js reads those arrays
  └── renders chart on <canvas> element
```

The three data fields map to chart axes and groupings like this:

| Model Field | Django Label | Chart Role |
|---|---|---|
| `field_1` | User-defined (e.g. "Amount") | Y-axis numeric value |
| `field_2` (category) | User-defined (e.g. "Type") | Series grouping / X-axis labels |
| `field_3` (date) | User-defined (e.g. "Date") | X-axis for time-series charts |

Because the field labels themselves are user-defined (stored in `FieldNames`), the chart axis titles also update dynamically to match whatever the user named their columns when they created the table.

#### Chart Types

The dashboard supports multiple chart types that the user can switch between using a dropdown — all reading from the same underlying data arrays:

| Chart Type | Best Used For |
|---|---|
| **Bar Chart** | Comparing numeric values across categories |
| **Line Chart** | Showing trends in numeric values over time (by date) |
| **Pie / Doughnut Chart** | Showing proportion of total by category |

Each chart type is instantiated as a `new Chart(ctx, { type: '...', data: {...}, options: {...} })` call. On dropdown change, the existing chart instance is destroyed with `chart.destroy()` and a new one is created with the selected type — this prevents Chart.js canvas conflicts between re-renders.

#### Dropdown-Driven Dynamic Switching

The chart type selector is a `<select>` element. A JavaScript `addEventListener('change', ...)` on it triggers the chart swap without any page reload:

```
User selects chart type from dropdown
      ↓
JS change event fires
      ↓
chart.destroy()   ← clears existing Chart.js instance from canvas
      ↓
new Chart(ctx, { type: selectedType, data: sharedData, options: sharedOptions })
      ↓
New chart renders instantly on same <canvas>
```

The data arrays (`labels`, `datasets`) are defined once at the top of the script block and reused across all chart types, so switching types never re-fetches data from the server.

#### Chart.js Configuration Highlights

- **Responsive layout** — `responsive: true` and `maintainAspectRatio: false` are set so the chart scales cleanly within its Tailwind CSS container.
- **Custom tooltips** — tooltips show the user's own field label names (pulled from `FieldNames` via DTL) rather than generic "Label" / "Value" text.
- **Legend** — displayed above the chart; labels correspond to the `field_2` category values present in the data.
- **Colour palette** — a fixed array of distinct colours is cycled across datasets/categories so each category gets a consistent colour regardless of how many exist.

### Export

- Users can export their table data to **PDF**, **CSV**, or **Excel** formats directly from the dashboard.

### UX Enhancements

- **Real-time form validation** on the registration page — JavaScript `EventListeners` fire `fetch()` calls to `validate-username` and `validate-email` on each keystroke. Each field shows a coloured tick/cross and an inline error message. The submit button is only enabled once every field passes validation.
- **Django Messages Framework** — success (green) and error (red) messages are displayed after every significant action (login, logout, data added, data deleted, etc.) using the `messages.html` partial.
- **Pagination** — long data tables are paginated for readability.
- **Search** — users can search within a table's records.
- **Sidebar navigation** — lists all of the user's tables by name; clicking switches the dashboard to that table's data.
- **Custom 404 page** — registered via `handler404`.

---

## Templates & UI

| Template | Purpose |
|---|---|
| `base.html` | Main layout — sidebar, navbar, messages block, content block |
| `base_auth.html` | Minimal layout for auth pages (no sidebar) |
| `main.html` | Public landing page shown to unauthenticated visitors |
| `messages.html` | Reusable partial for Django messages with colour coding |
| `partials/sidebar.html` | Lists user's tables; highlights active table |
| `partials/modal.html` | Reusable delete confirmation modal |
| `records/records.html` | Main dashboard — data table, search, pagination, export buttons, Chart.js `<canvas>`, chart-type dropdown, and inline JS data serialisation from DTL |
| `records/add-table.html` | Create new table form with optional first-row inline |
| `records/add-table-data.html` | Add data row form |
| `records/edit-table-data.html` | Edit data row form (pre-populated) |
| `authentication/register.html` | Registration form with real-time JS field validation |
| `authentication/login.html` | Login form |
| `authentication/reset-password.html` | Request password reset by email |
| `authentication/set-new-password.html` | Set new password via reset link |
| `errors/error404.html` | Custom 404 error page |

---

## Configuration & Environment Variables

Sensitive credentials are stored in a `.env` file at the project root (never committed to version control). They are loaded in `settings.py` via `python-dotenv`.

Create a `.env` file with the following keys:

```env
# MySQL Database
DB_NAME=your_database_name
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

# SMTP Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Google OAuth (via django-allauth)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- MySQL Server running locally
- A virtual environment tool (`venv` or `pipenv`)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/dashboardz.git
   cd dashboardz
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database**

   Open MySQL Workbench, create a new schema (e.g. `dashboardz`), and run the following to create the required tables manually (since `managed = False`):

   ```sql
   CREATE TABLE records_name (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(45) UNIQUE,
       owner VARCHAR(150) NOT NULL
   );

   CREATE TABLE field_names (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       field_1 VARCHAR(45),
       field_2 VARCHAR(45),
       field_3 VARCHAR(45),
       records_name_id BIGINT NOT NULL,
       owner VARCHAR(150) NOT NULL
   );

   CREATE TABLE field_2_names (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(45) NOT NULL,
       records_name_id BIGINT NOT NULL,
       owner VARCHAR(150) NOT NULL,
       UNIQUE KEY unique_name_per_record (records_name_id, name)
   );

   CREATE TABLE field_values (
       id BIGINT AUTO_INCREMENT PRIMARY KEY,
       field_1 DECIMAL(20,3) NOT NULL,
       field_2_id BIGINT NOT NULL,
       field_3 DATE NOT NULL,
       description TEXT NOT NULL,
       owner VARCHAR(150) NOT NULL,
       records_name_id BIGINT NOT NULL
   );
   ```

5. **Create the `.env` file** with your credentials (see [Configuration](#configuration--environment-variables)).

6. **Apply Django migrations** (for Django-managed tables like `auth_user`, sessions, etc.)
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Set up the Django Sites framework** (required for allauth)

   Log in to `/admin/`, go to **Sites**, and set the domain to `127.0.0.1:8000`.

9. **Configure Google OAuth** (optional)

   Go to [Google Cloud Console](https://console.cloud.google.com/), create OAuth 2.0 credentials, add `http://127.0.0.1:8000/accounts/google/login/callback/` as an authorised redirect URI, then add the credentials in `/admin/` under **Social Applications**.

---

## Running the Project

```bash
python manage.py runserver
```

The app will be available at: `http://127.0.0.1:8000/`

Django admin: `http://127.0.0.1:8000/admin/`

> **Note:** `DEBUG = True` and `ALLOWED_HOSTS = ["*"]` are set for development. Before deploying to production, set `DEBUG = False`, restrict `ALLOWED_HOSTS`, rotate the `SECRET_KEY`, and serve static files properly.

---



# Author
**Vaibhav Tiwari**
Punjab Engineering College
