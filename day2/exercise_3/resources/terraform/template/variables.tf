variable "admin_user" {
  type = string
  description = "Admin user for the image we're launching"
}

variable "admin_key_public" {
  type = string
  description = "Public SSH key of admin user"
}

variable "openstack_username" {
  type = string
  description = "Username to authenticate in Openstack."
}

variable "openstack_password" {
  type = string
  description = "Password to authenticate in Openstack."
}

variable "openstack_tenant_name" {
  type = string
}

variable "openstack_auth_url" {
  type = string
}

variable "openstack_region" {
  type = string
}

variable "openstack_user_domain_name" {
  type = string
}

variable "openstack_project_domain_name" {
  type = string
}

variable "external_network_id" {
  type = string
}

variable "network_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "image_id" {
  type = string
}

variable "flavor_id" {
  type = string
}
