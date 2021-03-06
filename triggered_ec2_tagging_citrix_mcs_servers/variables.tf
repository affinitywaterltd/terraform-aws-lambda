locals {
  environment_map = {
    dev = "dev"
    sit = "dev"
    uat = "prod"
    prod = "prod"
  }
}

variable "account" {}
variable "environment" {}

data "terraform_remote_state" "core" {
  backend = "remote"

  config = {
    organization = "AffinityWater"
    workspaces = {
      name =  "${var.account}-core-${lookup(local.environment_map, var.environment, "prod")}"
    }
  }
}