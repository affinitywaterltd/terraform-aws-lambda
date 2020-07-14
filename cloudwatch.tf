resource "aws_cloudwatch_event_rule" "schedule_start_of_month" {
  name                = "schedule_start_of_month"
  description         = "Runs at the start of each calendar month"
  schedule_expression = "cron(0 1 1 * ? *)"
}

resource "aws_cloudwatch_event_rule" "schedule_daily" {
  name                = "schedule_daily"
  description         = "Runs daily"
  schedule_expression = "cron(0 1 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "schedule_multi_daily_0700_1500" {
  name                = "schedule_multi_daily_0700_1500"
  description         = "Runs twice daily (0715 and 1515)"
  schedule_expression = "cron(15 7,15 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "trigger_maintenance_window_task_registered" {
  name          = "trigger_maintenance_window_task_registered"
  description   = "Runs every time a maintenance window is updated"
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

resource "aws_cloudwatch_event_rule" "trigger_ec2_instance_state_pending" {
  name          = "trigger_ec2_instance_state_pending"
  description   = "Runs every time an EC2 Instance is created (status 'Pending')"
  event_pattern = <<PATTERN
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ],
  "detail": {
    "state": [
      "pending"
    ]
  }
}
  
PATTERN

}

