# AWS Monthly Report
module "monthly_report" {
  source      = "./monthly_report"
  account     = "${var.account}"
  environment = "${var.environment}"
}
