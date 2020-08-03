variable "cloudwatch_rule_name" {
}

variable "cloudwatch_rule_arn" {
}

### Snapshot Cleanup

resource "aws_lambda_function" "daily_aws_backup_expired_deletion" {
  function_name = "daily_aws_backup_expired_deletion"
  filename      = "${path.module}/daily_aws_backup_expired_deletion.zip"

  role             = aws_iam_role.lambda_aws_backup_cleanup_role.arn
  source_code_hash = filebase64sha256("${path.module}/daily_aws_backup_expired_deletion.zip")
  handler          = "daily_aws_backup_expired_deletion.lambda_handler"
  runtime          = "python3.8"

  description = "Deletes AWS Backup recovery points that have expired"

  tags = local.base_tags

  memory_size = 128
  timeout     = 300
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.daily_aws_backup_expired_deletion.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.cloudwatch_rule_arn
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "daily_aws_backup_expired_deletion" {
  target_id = "daily_aws_backup_expired_deletion"
  arn       = aws_lambda_function.daily_aws_backup_expired_deletion.arn
  rule      = var.cloudwatch_rule_name
}

