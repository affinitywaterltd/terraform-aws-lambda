variable "cloudwatch_rule_name" {
}

variable "cloudwatch_rule_arn" {
}

### Update Maintenance Window Parameters

resource "aws_lambda_function" "daily_rds_check_free_space" {
  function_name = "daily_rds_check_free_space"
  filename      = "${path.module}/daily_rds_check_free_space.zip"

  role             = data.terraform_remote_state.core.outputs.lambda_report_role
  source_code_hash = filebase64sha256("${path.module}/daily_rds_check_free_space.zip")
  handler          = "daily_rds_check_free_space.lambda_handler"
  runtime          = "python3.7"

  description = "Checks the free space on all RDS instances and sends notifications using SNS"

  tags = local.base_tags

  memory_size = 128
  timeout     = 10

  environment {
    variables = {
      account = "false"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.daily_rds_check_free_space.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.cloudwatch_rule_arn
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "monthly_cloudwatch_logs_expiration" {
  target_id = "monthly_cloudwatch_logs_expiration"
  arn       = aws_lambda_function.daily_rds_check_free_space.arn
  rule      = var.cloudwatch_rule_name
}

