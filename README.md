# Company Birthday Tracker — Technical Report

A secure Internal service for tracking employee birthdays, featuring a Streamlit web interface and a FastAPI backend with integrated monitoring and automated IaC deployment.
(ДОБАВИТЬ ВЕЗДЕ ПЕРЕМЕННУЮ ДЛЯ JWT, УТУТ ОПИСАТЬ И В ДОКЕР КОМПОЗ)

## Team
- Sofia Palkina (s.palkina@innopolis.university)
- Amir Bairamov (a.bairamov@innopolis.university)
- Polina Kostikova (p.kostikova@innopolis.university)

## Project Access Points (Cloud)

- **Web Application:** [http://birthday-tracker.duckdns.org:8501](http://birthday-tracker.duckdns.org:8501/)
- **API Docs (Swagger):** [http://birthday-tracker.duckdns.org:8000/docs](http://birthday-tracker.duckdns.org:8000/docs)
- **Grafana Dashboards:** [http://birthday-tracker.duckdns.org:3000](http://birthday-tracker.duckdns.org:3000/)
- **Monitoring Tools:** [Prometheus (9090)](http://birthday-tracker.duckdns.org:9090/) | [Alertmanager (9093)](http://birthday-tracker.duckdns.org:9093/)

---

## 1. Introduction (Goal & Scope)

The **Company Birthday Tracker** was developed to solve the problem of fragmented and insecure employee birthday management. The project provides a centralized MVP service to:
- **Centralize Data:** Securely store and manage employee records (add/edit/delete).
- **Increase Visibility:** Provide a user-friendly view of birthdays for today and the next 7 days.
- **Ensure Security:** Protect data with JWT-based authentication and automated vulnerability scanning.
- **Maintain Reliability:** Monitor system health and hardware utilization in real-time.

---

## 2. Methods (Architecture & Implementation)

### 2.1 System Architecture
The application follows a microservices-inspired architecture deployed via Docker Compose on Yandex Cloud.
![](./docs/diagram.png)

### 2.2 Tech Stack
- **Backend:** FastAPI with SQLite.
- **Frontend:** Streamlit.
- **IaC:** Terraform Cloudmanaging Yandex Cloud Compute instances.
- **Observability:** Prometheus, Grafana, and Alertmanager.
- **Security:** JWT Authentication, Bandit (code scan), and Checkov (IaC scan).

---

## 3. Results (Implementation & Observability)

### 3.1 Functional Capabilities
- **Auth Flow:** Secure Login/Registration via JWT.
- **Search:** Real-time search of employees by full name.
- **Persistence:** Local SQLite storage mapped to Docker volumes for data durability.

### 3.2 Monitoring Metrics
The system tracks the following key performance indicators (KPIs):
- **HTTP Latency:** P95/P99 latency per API path.
- **Error Rates:** Ratio of 5xx errors to total requests.
- **System Health:** CPU (rate) and Memory (RSS) utilization via `metrics.py`.
- **Availability:** Auto-alerts via `Alertmanager` if the backend is unreachable for >1 minute.

### 3.3 Quality Assurance
The CI pipeline ensures all code meets the following standards:
- **Linting:** Flake8 (PEP8 compliance).
- **Coverage:** Pytest suite with `pytest-cov` (target > 20% for MVP).
- **Security:** Zero high-severity issues found by Bandit.

---

## 4. Discussion (Limitations & Future Work)

### 4.1 Limitations
- **Scaling:** SQLite is restricted to a single-node deployment.
- **Notifications:** - **Notifications:** Alertmanager is currently configured with a `noop` receiver; integration with real notification channels (e.g., email or messengers) is planned.

### 4.2 Future Directions
- **Database Migration:** Move to PostgreSQL for better concurrency.
- **Advanced Auth:** Implement Role-Based Access Control (RBAC).
- **Integration:** Add automated birthday greetings via Slack Webhooks.

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

# (Optional) Manually initialize database (usually not needed)
poetry run python scripts/init_db.py

# Install pre-commit hooks
poetry run pre-commit install
```
> The database is automatically initialized on backend startup (both locally and in Docker)

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
