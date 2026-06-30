# Plant Sync

A web application for logging and tracking maintenance issues across an industrial
plant site. Staff and contractors can register, raise issues against plant areas,
assign priorities, and track each issue through its lifecycle (open → in progress →
under review → closed).

> **Status: work in progress.** Core authentication and issue creation are working;
> the dashboard listing and role-based permissions are actively being built out.

## Features

- **User accounts** with role types (Contractor, Plant Management, Admin)
- **Secure authentication** — salted password hashing and session management via Flask-Login
- **Issue tracking** — description, area, submitter, assignee, status, and priority
- **Database migrations** managed with Alembic / Flask-Migrate
- **Responsive UI** built on Bootstrap 5 with a custom theme

## Tech stack

| Layer     | Technology                                  |
|-----------|---------------------------------------------|
| Backend   | Python, Flask                               |
| Database  | SQLAlchemy 2.0 ORM, SQLite                  |
| Migrations| Alembic (Flask-Migrate)                     |
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
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The app reads configuration from environment variables (with sensible defaults for
local development):

| Variable             | Description                          | Default                  |
|----------------------|--------------------------------------|--------------------------|
| `FLASK_SECRET_KEY`   | Session signing key                  | a dev placeholder        |
| `FLASK_DATABASE_URI` | SQLAlchemy database URI              | local SQLite file        |

For anything beyond local development, set a real `FLASK_SECRET_KEY`.

### Database setup

```bash
flask db upgrade
```

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
├── migrations/            # Alembic migration scripts
├── config.py              # Configuration
└── requirements.txt
```

## Roadmap

- [ ] Render the issues table on the dashboard
- [ ] Enforce role-based permissions (contractor vs. management vs. admin)
- [ ] Replace integer `submitted_by` / `completed_by` / `area` fields with proper relationships
- [ ] Edit and close issues from the dashboard
- [ ] Filtering and sorting of issues
- [ ] Automated tests (pytest)

## License

This project is for portfolio / educational purposes.
