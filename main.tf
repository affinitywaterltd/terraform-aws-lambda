
# AWS Monthly Report
/*
module "monthly_aws_cost_report" {
  source      = "./monthly_aws_cost_report"
  account     = "${var.account}"
  environment = "${var.environment}"
  cloudwatch_rule_name = "${aws_cloudwatch_event_rule.schedule_start_of_month.name}"
  cloudwatch_rule_arn = "${aws_cloudwatch_event_rule.schedule_start_of_month.arn}"
  ses_smtp_user = "${var.ses_smtp_user}"
  ses_smtp_password = "${var.ses_smtp_password}"
}
*/