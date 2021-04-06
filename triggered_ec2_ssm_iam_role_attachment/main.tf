variable "cloudwatch_rule_name" {
}

variable "cloudwatch_rule_arn" {
}

### Update Maintenance Window Parameters

resource "aws_lambda_function" "triggered_ec2_ssm_iam_role_attachment" {
  function_name = "triggered_ec2_ssm_iam_role_attachment"
  filename      = "${path.module}/triggered_ec2_ssm_iam_role_attachment.zip"

  role = aws_iam_role.lambda_ec2_ssm_iam_role.arn
  source_code_hash = filebase64sha256(
    "${path.module}/triggered_ec2_ssm_iam_role_attachment.zip",
  )
  handler = "triggered_ec2_ssm_iam_role_attachment.lambda_handler"
  runtime = "python3.8"

  description = "Add SSM role to new instances without a IAM role attached"

  tags = local.base_tags

  memory_size = 128
  timeout     = 300

  environment {
    variables = {
      role_name = "ssm_role"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.triggered_ec2_ssm_iam_role_attachment.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.cloudwatch_rule_arn
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "triggered_ec2_ssm_iam_role_attachment" {
  target_id = "triggered_ec2_ssm_iam_role_attachment"
  arn       = aws_lambda_function.triggered_ec2_ssm_iam_role_attachment.arn
  rule      = var.cloudwatch_rule_name
}

