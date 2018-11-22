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
