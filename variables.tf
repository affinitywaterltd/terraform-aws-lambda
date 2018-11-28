# Account settings 

variable "account" {}
variable "environment" {}
variable "ses_smtp_user" {}
variable "ses_smtp_password" {}

### IAM Roles

data "terraform_remote_state" "core" {
  backend = "atlas"

  config {
    name = "AffinityWater/${var.account}-core-${var.environment}"
  }
}