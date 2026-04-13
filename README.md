# Company Birthday Tracker

A simple internal service to track employee birthdays, with a web interface and API.

## Project Goal

The goal of this project is to provide an MVP application that allows a company to:

- store basic employee data,
- manage employee records (add/edit, optional delete),
- view upcoming birthdays (today + next 7 days),
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
├─ scripts/
├─ tests/
├─ docs/
├─ .gitignore
├─ pyproject.toml
└─ README.md
```
