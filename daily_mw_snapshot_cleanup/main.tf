variable "cloudwatch_rule_name" {
}

variable "cloudwatch_rule_arn" {
}

### Snapshot Cleanup

resource "aws_lambda_function" "auto_daily_mw_snapshot_cleanup" {
  function_name = "auto_daily_mw_snapshot_cleanup"
  filename      = "${path.module}/auto_daily_mw_snapshot_cleanup.zip"

  role             = data.terraform_remote_state.core.outputs.lambda_snapshot_cleanup_role
  source_code_hash = filebase64sha256("${path.module}/auto_daily_mw_snapshot_cleanup.zip")
  handler          = "auto_daily_mw_snapshot_cleanup.lambda_handler"
  runtime          = "python3.8"

  description = "Deletes AMIs/snapshots older than 14 tags if name starts with MaintenanceWindow"

  tags = local.base_tags

  memory_size = 128
  timeout     = 300
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auto_daily_mw_snapshot_cleanup.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.cloudwatch_rule_arn
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "auto_daily_mw_snapshot_cleanup" {
  target_id = "auto_daily_mw_snapshot_cleanup"
  arn       = aws_lambda_function.auto_daily_mw_snapshot_cleanup.arn
  rule      = var.cloudwatch_rule_name
}

