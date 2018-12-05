resource "aws_cloudwatch_event_rule" "schedule_start_of_month" {
  name        = "schedule_start_of_month"
  description = "Runs at the start of each calendar month"
  schedule_expression = "cron(34 11 5 * ? *)"
}