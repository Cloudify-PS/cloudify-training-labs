terraform {
  required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.35.0"
    }
    template = {
      source = "hashicorp/template"
      version = "2.1.2"
    }
  }
}

# Configure the OpenStack Provider
provider "openstack" {
  user_name           = var.openstack_username 
  tenant_name         = var.openstack_tenant_name
  password            = var.openstack_password
  auth_url            = var.openstack_auth_url
  region              = var.openstack_region
  user_domain_name    = var.openstack_user_domain_name
  project_domain_name = var.openstack_project_domain_name
}

# Fetch an external network
data "openstack_networking_network_v2" "external_network" {
  name            = var.external_network_id
  external        = "true"
}

# Fetch a private network
data "openstack_networking_network_v2" "example_network" {
  name            = var.network_id
}

# Fetch a subnet to launch our instances into
data "openstack_networking_subnet_v2" "example_subnet" {
  name              = var.subnet_id
  network_id        = data.openstack_networking_network_v2.example_network.id
}

# Security group for our application.
resource "openstack_networking_secgroup_v2" "example_security_group" {
  name        = "example_security_group"
  description = "Security group for example application"
}

resource "openstack_networking_secgroup_rule_v2" "secgroup_rule_ssh" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.example_security_group.id
}

resource "openstack_networking_secgroup_rule_v2" "secgroup_rule_http" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 80
  port_range_max    = 80
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.example_security_group.id
}

resource "openstack_networking_port_v2" "example_port" {
  name           = "example_port"
  network_id     = data.openstack_networking_network_v2.example_network.id
  admin_state_up = "true"
  
  fixed_ip {
    subnet_id = data.openstack_networking_subnet_v2.example_subnet.id
  }

  security_group_ids = [openstack_networking_secgroup_v2.example_security_group.id]
}

resource "openstack_networking_floatingip_v2" "ip" {
  pool    = data.openstack_networking_network_v2.external_network.name
  port_id = openstack_networking_port_v2.example_port.id
}

variable "filename" {
  default = "cloud-config.cfg"
}

data "template_file" "template" {
  template = <<EOF
#cloud-config
users:
  - name: $${admin_user}
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh-authorized-keys:
      - $${admin_key_public}
EOF
  vars = {
    admin_user = var.admin_user
    admin_key_public = var.admin_key_public
  }
}

resource "openstack_compute_instance_v2" "example_vm" {
  name = "example_vm"
  image_id = var.image_id
  flavor_id = var.flavor_id
  security_groups = [openstack_networking_secgroup_v2.example_security_group.id]

  network {
    port = openstack_networking_port_v2.example_port.id
  }

  user_data = data.template_file.template.rendered
}