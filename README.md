# Company Birthday Tracker — Technical Report

A secure Internal service for tracking employee birthdays, featuring a Streamlit web interface and a FastAPI backend with integrated monitoring and automated IaC deployment.

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
- **Centralize Data:** Store and manage employee records (add/edit/delete).
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

The MVP implementation delivers a comprehensive set of features focused on employee data lifecycle and data visibility:

- **Identity & Access Management:**
    - **JWT-based Authentication:** Implemented using FastAPI Security  with OAuth2 Bearer tokens. Password security is ensured via `bcrypt` hashing (passlib).
    - **Session Persistence:** The Streamlit frontend manages state using `st.session_state`, ensuring users remain authenticated across different tabs (Today/Upcoming/Profile).

- **Birthday Discovery & Visualization:**
    - **Dynamic Filtering:** Specialized API endpoints (/birthdays/today and /birthdays/upcoming) provide filtered views based on the server's current date.
    - **Global Search:** A full-name search feature using SQL `LIKE` patterns allows finding any colleague across the entire database, regardless of their birthday proximity.

- **Self-Service Profile Management:**
    - **CRUD Operations:** Authenticated users can update their own full name and birth date or completely delete their account, providing full data control for the employee.
    - **Input Validation:** Strict Pydantic schemas validate that birth dates are in the past and follow the ISO YYYY-MM-DD format.

- **Backend Reliability & Persistence:**
    - **Data Durability:** Using a mapped SQLite volume (`/app/data`), employee records survive container restarts and updates.
    - **Auto-Initialization:** The system features a custom startup event that triggers building the database schema (schema.sql) and seeding it with initial data if no database is detected.

### 3.2 Monitoring Metrics

The system tracks the following key performance indicators (KPIs) via Grafana dashboards:

- **Backend Up:** Service availability status.
- **HTTP Requests (rate) by path:** Number of HTTP requests per second for each API path.
- **5xx Error Rate (ratio):** Proportion of 5xx errors to total requests.
- **P95 Latency (per path):** 95th percentile of HTTP request latency per path.
- **P99 Latency (per path):** 99th percentile of HTTP request latency per path.
- **Process Memory (RSS):** Real-time RAM usage by the backend process.
- **Process CPU (rate):** Real-time CPU usage by the backend process.

All metrics are collected by Prometheus and visualized in Grafana on the **Backend Overview** dashboard.

### 3.3 Quality Assurance
The CI pipeline ensures all code meets the following standards:
- **Linting:** Flake8 (PEP8 compliance).
- **Coverage:** Pytest suite with `pytest-cov` (target > 20% for MVP).
- **Security:** Zero high-severity issues found by Bandit.

---

## 4. Discussion (Limitations & Future Work)

### 4.1 Limitations
- **Scaling:** SQLite is restricted to a single-node deployment.
- **Notifications:** Alertmanager is currently configured with a `noop` receiver; integration with real notification channels (e.g., email or messengers) is planned.

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

**Windows (PowerShell):**
```powershell
$env:GF_SECURITY_ADMIN_PASSWORD="your_secure_password"
$env:SECRET_KEY="your_long_random_jwt_secret"
docker compose up -d --build
```

**Linux / macOS:**
```bash
export GF_SECURITY_ADMIN_PASSWORD="your_secure_password"
export SECRET_KEY="your_long_random_jwt_secret"
docker compose up -d --build
```

> In production (Terraform Cloud), these credentials are set via **Sensitive Environment Variables** in the workspace settings. Please contact our team to obtain the Grafana access password.


---
