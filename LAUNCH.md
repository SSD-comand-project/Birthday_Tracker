
## Developer Guide: How to run the application locally

### 1. Requirements
- Python 3.10+ (recommended: 3.12)
- [Poetry](https://python-poetry.org/)
- Docker & Docker Compose

### 2. Setup and Installation
```bash
# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```


### 3. Running

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

> In production (Terraform Cloud), these credentials are set via **Sensitive Environment Variables** in the workspace settings.  Please contact our team to obtain the Grafana access password for production.

### 4. Service Endpoints

- **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
- **Backend (FastAPI docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Grafana (Monitoring Dashboard):** [http://localhost:3000](http://localhost:3000)
- **Prometheus:** [http://localhost:9090](http://localhost:9090)
- **Alertmanager:** [http://localhost:9093](http://localhost:9093)

---
