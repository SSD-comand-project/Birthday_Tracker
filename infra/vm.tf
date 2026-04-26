data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}

resource "yandex_compute_instance" "vm" {
  name        = "birthday-vm"
  platform_id = "standard-v2"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
      size     = 20
    }
  }

  # checkov:skip=CKV_YC_2: Public IP is required for accessing the application

  network_interface {
    subnet_id          = yandex_vpc_subnet.subnet.id
    security_group_ids = [yandex_vpc_security_group.sg.id]
    nat                = true
  }

  metadata = {
    ssh-keys = "ubuntu:${var.ssh_public_key}"

    user-data = <<EOF
#cloud-config

package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose
  - docker-compose-plugin
  - curl

write_files:
  - path: /app/docker-compose.yml
    permissions: '0644'
    content: |
      version: "3.9"

      services:
        backend:
          image: mrdebuff/birthday-backend:latest
          container_name: birthday-backend
          environment:
            - DB_PATH=/app/data/birthday_tracker.db
          volumes:
            - /app/data:/app/data
          ports:
            - "8000:8000"
          labels:
            - com.centurylinklabs.watchtower.enable=true
          restart: unless-stopped

        frontend:
          image: mrdebuff/birthday-frontend:latest
          container_name: birthday-frontend
          environment:
            - API_BASE_URL=http://backend:8000
          depends_on:
            - backend
          ports:
            - "8501:8501"
          labels:
            - com.centurylinklabs.watchtower.enable=true
          restart: unless-stopped

        prometheus:
          image: prom/prometheus:v2.45.0
          container_name: prometheus
          volumes:
            - /app/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
            - /app/monitoring/alerts.yml:/etc/prometheus/alerts.yml:ro
          command:
            - '--config.file=/etc/prometheus/prometheus.yml'
          ports:
            - "9090:9090"
          labels:
            - com.centurylinklabs.watchtower.enable=true
          restart: unless-stopped

        alertmanager:
          image: prom/alertmanager:v0.27.0
          container_name: alertmanager
          volumes:
            - /app/monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
          ports:
            - "9093:9093"
          labels:
            - com.centurylinklabs.watchtower.enable=true
          restart: unless-stopped

        grafana:
          image: grafana/grafana:latest
          container_name: grafana
          ports:
            - "3000:3000"
          volumes:
            - /app/monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
            - /app/monitoring/grafana/dashboards:/var/lib/grafana/dashboards:ro
          environment:
            - GF_SECURITY_ADMIN_PASSWORD=${var.grafana_admin_password}
            - GF_USERS_ALLOW_SIGN_UP=false
            - GF_DEFAULT_APP_HOME_DASHBOARD_UID=backend-overview
          labels:
            - com.centurylinklabs.watchtower.enable=true
          restart: unless-stopped

        watchtower:
          image: containrrr/watchtower
          container_name: watchtower
          volumes:
            - /var/run/docker.sock:/var/run/docker.sock
          command: --interval 60 --cleanup --label-enable
          labels:
            - com.centurylinklabs.watchtower.enable=false
          restart: unless-stopped

  - path: /app/monitoring/prometheus.yml
    permissions: '0644'
    content: |
      global:
        scrape_interval: 15s

      rule_files:
        - /etc/prometheus/alerts.yml

      alerting:
        alertmanagers:
          - static_configs:
              - targets: ['alertmanager:9093']

      scrape_configs:
        - job_name: 'backend'
          metrics_path: /metrics
          static_configs:
            - targets: ['backend:8000']

  - path: /app/monitoring/alerts.yml
    permissions: '0644'
    content: |
      groups:
        - name: backend.rules
          rules:
            - alert: BackendDown
              expr: up{job="backend"} == 0
              for: 1m
              labels:
                severity: critical
              annotations:
                summary: "Backend is down"
                description: "Prometheus cannot scrape backend /metrics for >1m"

            - alert: High5xxRate
              expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
              for: 5m
              labels:
                severity: warning
              annotations:
                summary: "High 5xx error rate"
                description: "High proportion of 5xx responses in last 5 minutes"

  - path: /app/monitoring/alertmanager.yml
    permissions: '0644'
    content: |
      global:
        resolve_timeout: 5m

      route:
        group_by: ['alertname']
        receiver: 'noop'

      receivers:
        - name: 'noop'

  - path: /app/monitoring/grafana/provisioning/datasources/datasource.yml
    permissions: '0644'
    content: |
      apiVersion: 1

      datasources:
        - name: Prometheus
          type: prometheus
          access: proxy
          url: http://prometheus:9090
          isDefault: true
          editable: false
          version: 1

  - path: /app/monitoring/grafana/provisioning/dashboards/dashboard.yml
    permissions: '0644'
    content: |
      apiVersion: 1

      providers:
        - name: 'default'
          orgId: 1
          folder: ''
          type: file
          disableDeletion: false
          editable: true
          options:
            path: /var/lib/grafana/dashboards

  - path: /app/monitoring/grafana/dashboards/backend.json
    permissions: '0644'
    content: |
      {
        "annotations": { "list": [] },
        "editable": true,
        "gnetId": null,
        "graphTooltip": 0,
        "id": null,
        "links": [],
        "panels": [
          {
            "type": "stat",
            "title": "Backend Up",
            "id": 1,
            "datasource": "Prometheus",
            "targets": [{ "expr": "up{job=\"backend\"}", "refId": "A" }],
            "gridPos": { "x": 0, "y": 0, "w": 24, "h": 4 }
          },
          {
            "type": "timeseries",
            "title": "HTTP requests (rate) by path",
            "id": 2,
            "datasource": "Prometheus",
            "targets": [{ "expr": "sum(rate(http_requests_total[1m])) by (path)", "refId": "A" }],
            "gridPos": { "x": 0, "y": 4, "w": 16, "h": 8 }
          },
          {
            "type": "timeseries",
            "title": "5xx error rate (ratio)",
            "id": 3,
            "datasource": "Prometheus",
            "targets": [
              { "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))", "refId": "A" }
            ],
            "gridPos": { "x": 16, "y": 4, "w": 8, "h": 8 }
          },
          {
            "type": "timeseries",
            "title": "P95 latency (per path)",
            "id": 4,
            "datasource": "Prometheus",
            "targets": [
              { "expr": "histogram_quantile(0.95, sum(rate(http_request_latency_seconds_bucket[5m])) by (le, path))", "refId": "A" }
            ],
            "gridPos": { "x": 0, "y": 12, "w": 12, "h": 8 }
          },
          {
            "type": "timeseries",
            "title": "P99 latency (per path)",
            "id": 5,
            "datasource": "Prometheus",
            "targets": [
              { "expr": "histogram_quantile(0.99, sum(rate(http_request_latency_seconds_bucket[5m])) by (le, path))", "refId": "A" }
            ],
            "gridPos": { "x": 12, "y": 12, "w": 12, "h": 8 }
          },
          {
            "type": "timeseries",
            "title": "Process memory (RSS)",
            "id": 9,
            "datasource": "Prometheus",
            "targets": [{ "expr": "process_resident_memory_bytes{job=\"backend\"}", "refId": "A" }],
            "gridPos": { "x": 0, "y": 20, "w": 12, "h": 6 }
          },
          {
            "type": "timeseries",
            "title": "Process CPU (rate)",
            "id": 10,
            "datasource": "Prometheus",
            "targets": [{ "expr": "rate(process_cpu_seconds_total{job=\"backend\"}[1m])", "refId": "A" }],
            "gridPos": { "x": 12, "y": 20, "w": 12, "h": 6 }
          }
        ],
        "schemaVersion": 36,
        "title": "Backend Overview",
        "uid": "backend-overview",
        "version": 2,
        "time": { "from": "now-1h", "to": "now" }
      }

  - path: /app/update-duckdns.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      curl "https://www.duckdns.org/update?domains=${var.duckdns_domain}&token=${var.duckdns_token}&ip="

runcmd:
  - mkdir -p /app/data
  - mkdir -p /app/monitoring/grafana/provisioning/datasources
  - mkdir -p /app/monitoring/grafana/provisioning/dashboards
  - mkdir -p /app/monitoring/grafana/dashboards
  - usermod -aG docker ubuntu
  - systemctl enable docker
  - systemctl start docker
  - cd /app

  # Run Docker Compose
  - docker compose -f /app/docker-compose.yml pull
  - docker compose -f /app/docker-compose.yml up -d

  # First run of DuckDNS
  - /app/update-duckdns.sh

  # Cron for DuckDNS every 5 minutes
  - echo "*/5 * * * * root /app/update-duckdns.sh" > /etc/cron.d/duckdns
  - chmod 644 /etc/cron.d/duckdns
  - systemctl restart cron
EOF
  }
}
