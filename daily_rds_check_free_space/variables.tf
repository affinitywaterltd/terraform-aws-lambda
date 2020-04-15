variable "account" {
}

variable "environment" {
}

variable "sns_sms_list_info" {
  default = []
}

variable "sns_sms_list_warn" {
  default = []
}

data "terraform_remote_state" "core" {
  backend = "atlas"

  config = {
    name = "AffinityWater/${var.account}-core-${var.environment}"
  }
}

