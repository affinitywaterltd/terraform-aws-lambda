
variable "account" {}
variable "environment" {}

variable "sns_sms_list" {}

data "terraform_remote_state" "core" {
  backend = "atlas"

  config {
    name = "AffinityWater/${var.account}-core-${var.environment}"
  }
}