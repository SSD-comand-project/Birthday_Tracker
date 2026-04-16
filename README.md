# Company Birthday Tracker

A simple internal service to track employee birthdays, with a web interface and API.

## Project Goal

The goal of this project is to provide an MVP application that allows a company to:

- store basic employee data,
- manage employee records (add/edit, optional delete),
- view upcoming birthdays (today + next 7 days),
- search employees by full name to see they birthdays,
- protect management functionality with basic authentication.

---

## MVP Scope

### Included

- Employee management:
  - Add employee manually
  - Edit employee manually
  - (Optional) Delete employee
- Upcoming birthdays:
  - Employees with birthdays **today**
  - Employees with birthdays in the **next 7 days**
- Basic admin authentication (username/password)
- SQLite as a simple local database
- Streamlit frontend + Python backend API
- Terraform-based infrastructure configuration
- CI checks for IaC quality/security:
  - `terraform fmt -check`
  - `tflint`
  - `checkov`


## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python (API)
- **Database:** SQLite
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions
- **IaC quality/security checks:** `terraform fmt`, `tflint`, `checkov`


## Repository Structure

```text
company-birthday-tracker/
├─ app/
│  ├─ backend/
│  │  ├─ __init__.py
│  │  ├─ services/
│  │  │  ├─ __init__.py
│  │  │  ├─ users.py
│  │  │  └─ birthdays.py
│  │  ├─ routers/
│  │  │  └─ __init__.py
│  │  └─ utils/
│  │     ├─ __init__.py
│  │     └─ errors.py
│  └─ frontend/
├─ infra/
│  ├─ terraform/
│  └─ diagrams/
├─ monitoring/
│  ├─ healthcheck/
│  └─ alerts/
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ data/ #db
├─ scripts/
│  └─ init_db.py
├─ tests/
│  └─ test_services.py
├─ docs/
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
├─ poetry.lock
├─ requirements.txt
├─ .bandit
├─ .pre-commit-config.yaml
├─ .flake8
└─ README.md
```
## Developer Guide

### 1. Requirements

- Python 3.10+ (recommended: 3.12)
- [Poetry](https://python-poetry.org/)
- (Optional) `sqlite3` CLI for manual DB checks

---

### 2. Install dependencies

```bash
poetry install # --no-root
```

If dependencies were changed:

```bash
poetry lock
poetry install
```

---

### 3. Initialize database

Database file is stored at `data/birthday_tracker.db` by default.

```bash
poetry run python scripts/init_db.py
```

You can override DB path with env variable:

```bash
# Linux/macOS
export DB_PATH=./data/test.db

# Windows PowerShell
$env:DB_PATH = ".\data\test.db"
```

---

### 4. Run application

#### FastAPI backend
```bash
poetry run uvicorn app.backend.main:app --reload
```

#### Streamlit frontend
```bash
poetry run streamlit run app/frontend/streamlit_app.py
```

---

### 5. Run tests

```bash
poetry run pytest -v
```

With coverage:

```bash
poetry run pytest tests --cov=app --cov-report=term-missing --cov-report=xml -v
```

---

### 6. Pre-commit hooks

Install hooks once:

```bash
poetry run pre-commit install
```

Run manually on all files:

```bash
poetry run pre-commit run --all-files
```

---

### 7. Lint and security checks

```bash
poetry run flake8 app/
poetry run bandit -r app/ -ll
poetry run radon cc -a -s -n B app/
poetry run radon mi -s app/
```

---

### 8. SQLite manual checks

Show all users:

```bash
sqlite3 ./data/birthday_tracker.db ".headers on" ".mode table" "SELECT id, username, full_name, birth_date, created_at, updated_at FROM users ORDER BY id;"
```
