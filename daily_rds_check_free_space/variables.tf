variable "account" {}
variable "environment" {}

variable "sns_sms_list_info" {
  default = []
}

variable "sns_sms_list_warn" {
  default = []
}

data "terraform_remote_state" "core" {
  backend = "remote"

  config = {
    organization = "AffinityWater"
    workspaces = {
      name =  "${var.account}-core-${lookup(local.environment_map, var.environment, "prod")}"
    }
  }
}