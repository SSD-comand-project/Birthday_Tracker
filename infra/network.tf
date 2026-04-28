resource "yandex_vpc_network" "net" {
  name = "birthday-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "birthday-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.net.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}
