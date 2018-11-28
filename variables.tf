# Account settings 

variable "account" {}
variable "environment" {}

### IAM Roles

data "terraform_remote_state" "core" {
  backend = "atlas"

  config {
    name = "AffinityWater/${var.account}-core-${var.environment}"
  }
}

variable "ses_smtp_user" {
  description = "Contains SES IAM User Access details - From TFE"
  default = "replace me"
}
variable "ses_smtp_password" {
  description = "Contains SES IAM User Access password - From TFE"
  default = "replace me"
}
