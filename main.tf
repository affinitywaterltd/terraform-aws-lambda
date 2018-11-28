# AWS Monthly Report
module "monthly_aws_cost_report" {
  source      = "./monthly_aws_cost_report"
  account     = "${var.account}"
  environment = "${var.environment}"
  cloudwatch_rule = "${aws_cloudwatch_event_rule.schedule_start_of_month.name}"
}
