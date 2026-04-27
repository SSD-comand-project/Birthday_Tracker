# Company Birthday Tracker

A secure Internal service to track employee birthdays, featuring a Streamlit web interface and a FastAPI backend with integrated monitoring.

## Application & Monitoring URLs

- **Web Application:** [http://birthday-tracker.duckdns.org:8501/](http://birthday-tracker.duckdns.org:8501/)
- **API Docs:** [http://birthday-tracker.duckdns.org:8000/docs](http://birthday-tracker.duckdns.org:8000/docs)
- **Grafana Dashboards:** [http://birthday-tracker.duckdns.org:3000/](http://birthday-tracker.duckdns.org:3000/)
- **Prometheus:** [http://birthday-tracker.duckdns.org:9090/](http://birthday-tracker.duckdns.org:9090/)
- **Alertmanager:** [http://birthday-tracker.duckdns.org:9093/](http://birthday-tracker.duckdns.org:9093/)

> ℹ️ For local development, use `localhost` instead of `birthday-tracker.duckdns.org`.


## Project Goal & Scope

The goal of this project is to provide a reliable MVP application for:
- **Employee Data Management:** Securely store and manage employee records (add/edit/delete).
- **Birthday Visibility:** View upcoming birthdays (today + next 7 days).
- **Search:** Quickly find colleagues by full name.
- **Security:** Protect management functionality with JWT-based authentication.
- **Observability:** Monitor system health via a dedicated metrics stack.

---

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **Infrastructure:** Terraform & Yandex Cloud
- **Monitoring:** Prometheus, Grafana, Alertmanager
- **CI/CD:** GitHub Actions & Terraform Cloud

---

## Monitoring & Observability

The application includes a self-hosted monitoring stack defined in `docker-compose.yml`:

- **Prometheus:** Scrapes application metrics from the backend's `/metrics` endpoint.
- **Grafana:** Visualizes metrics (HTTP rates, error ratios, system health).
  - *Default dashboard:* **Backend Overview**.
  - *Access:* `http://localhost:3000` (User: `admin`).
- **Alertmanager:** Handles alerts defined in `monitoring/alerts.yml` (e.g., checks if the Backend is down).

---

## Infrastructure (IaC)

We use **Terraform** for automated deployment to Yandex Cloud via **Terraform Cloud**.
- **Automated Workflow:** A Pull Request triggers `terraform plan`.
- **Security Checks:** Our CI pipeline runs `fmt`, `tflint`, and `checkov` to ensure cloud security best practices.
- **Secrets:** All sensitive keys (Grafana password, SSH keys) are managed as secure variables in Terraform Cloud.

---

## Developer Guide

### 1. Requirements
- Python 3.10+ (recommended: 3.12)
- [Poetry](https://python-poetry.org/)
- Docker & Docker Compose

### 2. Setup and Installation
```bash
# Install dependencies
poetry install

# Initialize database
poetry run python scripts/init_db.py

# Install pre-commit hooks
poetry run pre-commit install
```

### 3. Running Locally

#### Using Docker Compose (Recommended)
This starts the App, Database, and the full Monitoring stack:
```bash
# Set your Grafana password (or leave for default 'admin')
$env:GF_SECURITY_ADMIN_PASSWORD="your_password"
docker compose up -d --build
```
> ℹ️ In production (Terraform Cloud), the Grafana admin password is set via the `GF_SECURITY_ADMIN_PASSWORD` environment variable in the Terraform Cloud workspace settings. Please contact our team  to get the current password.


#### Manual Run (for Development)
```bash
# Backend
poetry run uvicorn app.backend.main:app --reload

# Frontend
poetry run streamlit run app/frontend/streamlit_app.py
```

---

## Quality, Security & Testing

We enforce high code standards through several tools:

- **Tests:** `poetry run pytest tests --cov=app`
- **Linting:** `poetry run flake8 app/` (PEP8 compliance)
- **Security:** `poetry run bandit -r app/ -ll` (Code vulnerability scan)
- **Complexity:** `poetry run radon cc -a -s app/` (Cyclomatic complexity)
- **Hooks:** Pre-commit hooks run automatically on every `git commit`.

---

## Repository Structure

```text
company-birthday-tracker/
├─ app/
│  ├─ backend/      # FastAPI API & Metrics
│  └─ frontend/     # Streamlit App
├─ infra/           # Terraform HCL files
├─ monitoring/      # Prometheus, Grafana, Alertmanager configs
├─ .github/         # CI/CD (GitHub Actions)
├─ data/            # Persistence (SQLite)
├─ scripts/         # DB Initialization
├─ tests/           # Pytest suite
└─ pyproject.toml   # Poetry & Tool configs
```
