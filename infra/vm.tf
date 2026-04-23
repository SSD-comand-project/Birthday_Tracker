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

runcmd:
  - apt-get update
  - apt-get install -y docker.io docker-compose
  - systemctl enable docker
  - systemctl start docker

  - mkdir -p /app
  - cd /app

  - echo '${file("${path.module}/../docker-compose.yml")}' > docker-compose.yml

  - docker-compose pull
  - docker-compose up -d
EOF
  }
}
