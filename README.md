# Company Birthday Tracker — Technical Report

A secure Internal service for tracking employee birthdays, featuring a Streamlit web interface and a FastAPI backend with integrated monitoring and automated IaC deployment.
(ДОБАВИТЬ ВЕЗДЕ ПЕРЕМЕННУЮ ДЛЯ JWT, УТУТ ОПИСАТЬ И В ДОКЕР КОМПОЗ)

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
- **Notifications:** Alertmanager is currently configured with a `noop` receiver; real email/Slack notification integration is pending.

### 4.2 Future Directions
- **Database Migration:** Move to PostgreSQL for better concurrency.
- **Advanced Auth:** Implement Role-Based Access Control (RBAC).
- **Integration:** Add automated birthday greetings via Slack Webhooks.

---

## Developer Guide (Local Setup)

```bash
# 1. Install dependencies
poetry install

# 2. Initialize database
poetry run python scripts/init_db.py

# 3. Run full stack locally
$env:GF_SECURITY_ADMIN_PASSWORD="admin"
docker compose up -d --build
```
