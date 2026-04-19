FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==1.8.3
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi --without dev --no-root

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app/frontend/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
