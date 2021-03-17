variable "account" {
}

variable "environment" {
}

data "terraform_remote_state" "core" {
  backend = "atlas"

  config = {
    name = "AffinityWater/${var.account}-core-${var.environment}"
  }
}

data "aws_caller_identity" "current" {}