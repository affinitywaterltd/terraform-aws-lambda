
variable "account" {}
variable "environment" {}

variable "sns_sms_list_info" {}

variable "sns_sms_list_warn" {}


data "terraform_remote_state" "core" {
  backend = "atlas"

  config {
    name = "AffinityWater/${var.account}-core-${var.environment}"
  }
}