# Plant Sync

A web application for logging and tracking maintenance issues across an industrial
plant site. Staff and contractors can register, raise issues against plant areas,
assign priorities, and track each issue through its lifecycle (open → in progress →
under review → closed).

> **Status: work in progress.** Login, registration, issue and area forms, and a
> filtered issue dashboard are present. The next steps are to secure account roles,
> finish issue management, and add automated checks before deployment.

## Features

- **User accounts** with role types (Contractor, Plant Management, Admin)
- **Secure authentication** — salted password hashing and session management via Flask-Login
- **Issue tracking** — description, area, submitter, assignee, status, and priority
- **Local database** stored in a SQLite file
- **Responsive UI** built on Bootstrap 5 with a custom theme

## Tech stack

| Layer     | Technology                                  |
|-----------|---------------------------------------------|
| Backend   | Python, Flask                               |
| Database  | SQLAlchemy 2.0 ORM with SQLite (`app/data/app.db`) |
| Forms     | Flask-WTF / WTForms (with CSRF protection)  |
| Auth      | Flask-Login, Werkzeug password hashing      |
| Frontend  | Jinja2, Bootstrap 5, custom CSS             |

## Getting started

### Prerequisites
- Python 3.11+

### Installation

```bash
# Clone the repository
git clone https://github.com/ajgartman/plant_sync.git
cd plant_sync

# Create and activate a virtual environment
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The app reads configuration from environment variables (with sensible defaults for
local development):

| Variable             | Description                          | Default                  |
|----------------------|--------------------------------------|--------------------------|
| `FLASK_SECRET_KEY`   | Session signing key                  | a dev placeholder        |

For anything beyond local development, set a real `FLASK_SECRET_KEY`. The SQLite
database is stored in `app/data/app.db`; that local data file is ignored by Git.

### Database setup

After installing dependencies, reset the old database to the current SQLAlchemy
models. The reset script first checks the database and saves a timestamped backup,
then recreates its tables. **This resets the app data**; existing users, areas, and
issues are retained only in the backup file.

```bash
python scripts/reset_database.py
```

Run this once, as you requested, and again only when you intentionally want to reset
the local database. Backups are saved beside it in `app/data/`.

For a new database without a backup/reset, run `flask --app app init-db`. This only
creates missing tables and does not update or clear existing ones.

### Running

```bash
flask run
```

Then open <http://127.0.0.1:5000> in your browser.

## Project structure

```
plant_sync/
├── app/
│   ├── __init__.py        # App, extensions, and config setup
│   ├── routes.py          # View functions / endpoints
│   ├── models.py          # SQLAlchemy models (User, Issues)
│   ├── forms.py           # WTForms form definitions
│   ├── static/            # CSS, images
│   └── templates/         # Jinja2 templates
├── config.py              # Configuration
└── requirements.txt
```

## Roadmap

The work is organized into small steps so the app stays easy to follow.

### 1. Make the core workflow reliable
- [x] Store app data in a local SQLite file at `app/data/app.db`
- [x] Register and log in users with hashed passwords
- [x] Add plant areas and create issues linked to an area and submitter
- [x] List issues and filter the dashboard by status
- [x] Back up and reset the older SQLite schema to match the current models
- [x] Show a helpful 404 for missing issue IDs and validate selected area IDs

### 2. Complete issue management
- [x] Let plant management and admins change status and completion details
- [x] Add a clear empty state when there are no issues
- [x] Show management navigation and controls only to management users
- [ ] Add simple search or sorting if it improves the main workflow

### 3. Make accounts and permissions safe
- [ ] Do not let public registration choose the admin or management role
- [ ] Restrict management pages and actions by account type
- [ ] Add friendly handling for duplicate usernames and invalid sign-in
- [ ] Use a private secret key outside local development

### 4. Prepare a CV-ready release
- [ ] Add focused tests for registration, login, area creation, issue creation, filtering, and access rules
- [x] Replace the placeholder home page with an operations dashboard and clearly labeled sample OEE gauges
- [ ] Collect runtime and production counts before presenting OEE as live data
- [ ] Document setup, sample workflow, and known limitations
- [ ] Run through the documented setup from a clean checkout
- [ ] Choose a hosting option and document deployment and database backups

## License

This project is for portfolio / educational purposes.
