variable "cloud_id" {
  description = "Yandex Cloud ID"
  type        = string
}

variable "folder_id" {
  description = "Yandex Cloud folder ID"
  type        = string
}

variable "zone" {
  description = "Availability zone"
  type        = string
  default     = "ru-central1-a"
}

variable "ssh_public_key" {
  description = "SSH public key content"
  type        = string
}

variable "duckdns_token" {
  description = "DuckDNS token"
  type        = string
  sensitive   = true
}

variable "duckdns_domain" {
  description = "DuckDNS domain (without .duckdns.org)"
  type        = string
}
