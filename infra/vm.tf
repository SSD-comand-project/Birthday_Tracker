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
          restart: unless-stopped

runcmd:
  - mkdir -p /app/data
  - systemctl enable docker
  - systemctl start docker
  - cd /app
  - docker-compose pull
  - docker-compose up -d
EOF
  }
}
