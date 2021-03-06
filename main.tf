# AWS Monthly Cost Report

module "monthly_aws_cost_report" {
  source               = "./monthly_aws_cost_report"
  account              = var.account
  environment          = var.environment
  cloudwatch_rule_name = aws_cloudwatch_event_rule.schedule_start_of_month.name
  cloudwatch_rule_arn  = aws_cloudwatch_event_rule.schedule_start_of_month.arn
  ses_smtp_user        = var.ses_smtp_user
  ses_smtp_password    = var.ses_smtp_password
}

# Daily snapshot cleanup

module "daily_mw_snapshot_cleanup" {
  source               = "./daily_mw_snapshot_cleanup"
  account              = var.account
  environment          = var.environment
  cloudwatch_rule_name = aws_cloudwatch_event_rule.schedule_daily.name
  cloudwatch_rule_arn  = aws_cloudwatch_event_rule.schedule_daily.arn
}

# Tag Citrix MCS Servers

module "triggered_ec2_tagging_citrix_mcs_servers" {
  source               = "./triggered_ec2_tagging_citrix_mcs_servers"
  account              = var.account
  environment          = var.environment
  cloudwatch_rule_name = aws_cloudwatch_event_rule.trigger_ec2_instance_state_pending.name
  cloudwatch_rule_arn  = aws_cloudwatch_event_rule.trigger_ec2_instance_state_pending.arn
}

# Configure CloudWatchLogs Expiration Policy

module "monthly_cloudwatch_logs_expiration" {
  source               = "./monthly_cloudwatch_logs_expiration"
  account              = var.account
  environment          = var.environment
  cloudwatch_rule_name = aws_cloudwatch_event_rule.schedule_start_of_month.name
  cloudwatch_rule_arn  = aws_cloudwatch_event_rule.schedule_start_of_month.arn
}

# Configure RDS Free Space Checker

module "daily_rds_check_free_space" {
  source               = "./daily_rds_check_free_space"
  account              = var.account
  environment          = var.environment
  cloudwatch_rule_name = aws_cloudwatch_event_rule.schedule_multi_daily_0700_1500.name
  cloudwatch_rule_arn  = aws_cloudwatch_event_rule.schedule_multi_daily_0700_1500.arn
  sns_sms_list_info    = var.sns_sms_list_rds_alerts_info
  sns_sms_list_warn    = var.sns_sms_list_rds_alerts_warn
}

module "daily_aws_backup_expired_deletion" {
  source               = "./daily_aws_backup_expired_deletion"
  account              = var.account
  environment          = var.environment
  cloudwatch_rule_name = aws_cloudwatch_event_rule.schedule_daily.name
  cloudwatch_rule_arn  = aws_cloudwatch_event_rule.schedule_daily.arn
}

# Maintenance Window Parameter Injection
/*
module "triggered_maintenance_window_parameter_injection" {
  source      = "./triggered_maintenance_window_parameter_injection"
  account     = "${var.account}"
  environment = "${var.environment}"
  cloudwatch_rule_name = "${aws_cloudwatch_event_rule.trigger_maintenance_window_task_registered.name}"
  cloudwatch_rule_arn = "${aws_cloudwatch_event_rule.trigger_maintenance_window_task_registered.arn}"
}
*/

module "triggered_ec2_ssm_iam_role_attachment" {
  source               = "./triggered_ec2_ssm_iam_role_attachment"
  account              = var.account
  environment          = var.environment
  cloudwatch_rule_name = aws_cloudwatch_event_rule.trigger_ec2_instance_state_pending.name
  cloudwatch_rule_arn  = aws_cloudwatch_event_rule.trigger_ec2_instance_state_pending.arn
}

module "ssm_start_stopped_instances" {
  source               = "./ssm_start_stopped_instances"
  account              = var.account
  environment          = var.environment

}