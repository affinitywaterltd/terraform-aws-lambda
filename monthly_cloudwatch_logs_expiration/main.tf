variable "cloudwatch_rule_name" {
}

variable "cloudwatch_rule_arn" {
}

### Update Maintenance Window Parameters

resource "aws_lambda_function" "auto_monthly_cloudwatch_logs_expiration" {
  function_name = "auto_monthly_cloudwatch_logs_expiration"
  filename      = "${path.module}/auto_monthly_cloudwatch_logs_expiration.zip"

  role             = data.terraform_remote_state.core.outputs.lambda_cloudwatch_logs_expiration_role
  source_code_hash = filebase64sha256("${path.module}/auto_monthly_cloudwatch_logs_expiration.zip")
  handler          = "auto_monthly_cloudwatch_logs_expiration.lambda_handler"
  runtime          = "python3.7"

  description = "Adds a retention policy to any CloudWatch Logs that are set to never expire. Can set overwrite variable to 'true' to force all logs to match retention policy settings"

  tags = local.base_tags

  memory_size = 128
  timeout     = 60

  environment {
    variables = {
      overwrite = "false"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auto_monthly_cloudwatch_logs_expiration.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.cloudwatch_rule_arn
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "monthly_cloudwatch_logs_expiration" {
  target_id = "monthly_cloudwatch_logs_expiration"
  arn       = aws_lambda_function.auto_monthly_cloudwatch_logs_expiration.arn
  rule      = var.cloudwatch_rule_name
}

