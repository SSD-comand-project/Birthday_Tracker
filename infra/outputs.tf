output "public_ip" {
  value = yandex_compute_instance.vm.network_interface[0].nat_ip_address
}

output "frontend_url" {
  value = "http://${yandex_compute_instance.vm.network_interface[0].nat_ip_address}:8501"
}

output "grafana_url" {
  value = "http://${yandex_compute_instance.vm.network_interface[0].nat_ip_address}:3000"
}

output "prometheus_url" {
  value = "http://${yandex_compute_instance.vm.network_interface[0].nat_ip_address}:9090"
}

output "alertmanager_url" {
  value = "http://${yandex_compute_instance.vm.network_interface[0].nat_ip_address}:9093"
}
