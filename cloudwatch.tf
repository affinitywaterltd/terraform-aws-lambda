resource "aws_cloudwatch_event_rule" "schedule_start_of_month" {
  name        = "schedule_start_of_month"
  description = "Runs at the start of each calendar month"
  schedule_expression = "cron(0 1 1 * ? *)"
  role_arn = "${data.terraform_remote_state.core.invoke_lambda_role}"
}