# Account settings 

variable "account" {
}

variable "environment" {
}

variable "ses_smtp_user" {
}

variable "ses_smtp_password" {
}

### IAM Roles

data "terraform_remote_state" "core" {
  backend = "atlas"

  config = {
    name = "AffinityWater/${var.account}-core-${var.environment}"
  }
}

# SNS Alerts
variable "sns_sms_list_rds_alerts_info" {
  description = "List of SMS addresses for SNS tpoic subscription - RDS Alerts"
  default     = []
}

variable "sns_sms_list_rds_alerts_warn" {
  description = "List of SMS addresses for SNS tpoic subscription - RDS Alerts"
  default     = []
}

