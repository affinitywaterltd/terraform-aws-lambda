variable "cloudwatch_rule_name" {
}

variable "cloudwatch_rule_arn" {
}

### Monthly report

resource "aws_lambda_function" "monthly_aws_cost_report" {
  function_name = "auto_monthly_aws_cost_report"
  filename      = "${path.module}/auto_monthly_aws_cost_report.zip"

  role             = aws_iam_role.lambda_aws_cost_report_role.arn
  source_code_hash = filebase64sha256("${path.module}/auto_monthly_aws_cost_report.zip")
  handler          = "auto_monthly_aws_cost_report.lambda_handler"
  runtime          = "python3.8"

  description = "Lists all the cost centre/quadrant for EC2 and RDS - emails and uploads to S3"

  tags = local.base_tags

  memory_size = 128
  timeout     = 300
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.monthly_aws_cost_report.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.cloudwatch_rule_arn
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "monthly_aws_cost_report_target" {
  target_id = "monthly_aws_cost_report"
  arn       = aws_lambda_function.monthly_aws_cost_report.arn
  rule      = var.cloudwatch_rule_name
}

