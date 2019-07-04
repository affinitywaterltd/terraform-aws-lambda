
# AWS Monthly Cost Report

module "monthly_aws_cost_report" {
  source      = "./monthly_aws_cost_report"
  account     = "${var.account}"
  environment = "${var.environment}"
  cloudwatch_rule_name = "${aws_cloudwatch_event_rule.schedule_start_of_month.name}"
  cloudwatch_rule_arn = "${aws_cloudwatch_event_rule.schedule_start_of_month.arn}"
  ses_smtp_user = "${var.ses_smtp_user}"
  ses_smtp_password = "${var.ses_smtp_password}"
}


# Daily snapshot cleanup

module "daily_mw_snapshot_cleanup" {
  source      = "./daily_mw_snapshot_cleanup"
  account     = "${var.account}"
  environment = "${var.environment}"
  cloudwatch_rule_name = "${aws_cloudwatch_event_rule.schedule_daily.name}"
  cloudwatch_rule_arn = "${aws_cloudwatch_event_rule.schedule_daily.arn}"
}

# Maintenance Window Parameter Injection

module "triggered_maintenance_window_parameter_injection" {
  source      = "./triggered_maintenance_window_parameter_injection"
  account     = "${var.account}"
  environment = "${var.environment}"
  cloudwatch_rule_name = "${aws_cloudwatch_event_rule.trigger_maintenance_window_task_registered.name}"
  cloudwatch_rule_arn = "${aws_cloudwatch_event_rule.trigger_maintenance_window_task_registered.arn}"
}