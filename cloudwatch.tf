resource "aws_cloudwatch_event_rule" "schedule_start_of_month" {
  name        = "schedule_start_of_month"
  description = "Runs at the start of each calendar month"
  schedule_expression = "cron(0 1 1 * ? *)"
}

resource "aws_cloudwatch_event_rule" "schedule_daily" {
  name        = "schedule_daily"
  description = "Runs daily"
  schedule_expression = "cron(0 1 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "trigger_maintenance_window_task_registered" {
  name        = "trigger_maintenance_window_task_registered"
  description = "Runs daily"
  event_pattern = <<PATTERN
{
  "source": [
    "aws.ssm"
  ],
  "detail-type": [
    "Maintenance Window Task Registration Notification"
  ]
}
  PATTERN
}