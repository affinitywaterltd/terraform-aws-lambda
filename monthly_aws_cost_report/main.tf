

variable "cloudwatch_rule_name" {}
variable "cloudwatch_rule_arn" {}

### Monthly report

resource "aws_lambda_function" "monthly_aws_cost_report" {
  function_name = "auto_monthly_aws_cost_report"
  filename      = "${path.module}/auto_monthly_aws_cost_report.zip"

  role             = "${data.terraform_remote_state.core.lambda_report_role}" 
  source_code_hash = "${base64sha256(file("${path.module}/auto_monthly_aws_cost_report.zip"))}"
  handler          = "auto_monthly_aws_cost_report.lambda_handler"
  runtime          = "python2.7"

  description = "Lists all the cost centre/quadrant for EC2 and RDS - emails and uploads to S3"

  tags = "${local.common_tags}"

  memory_size = 128
  timeout     = 300

  environment {
    variables = {
      smtp_ses_password = "${var.ses_smtp_password}"
      smtp_ses_user = "${var.ses_smtp_user}"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.monthly_aws_cost_report.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${var.cloudwatch_rule_arn}"
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "monthly_aws_cost_report_target" {
  target_id = "monthly_aws_cost_report"
  arn = "${aws_lambda_function.monthly_aws_cost_report.arn}"
  rule = "${var.cloudwatch_rule_name}"
}

