

variable "cloudwatch_rule" {}

### Monthly report

resource "aws_lambda_function" "monthly_aws_cost_report" {
  function_name = "auto_monthly_aws_cost_report"
  filename      = "${path.module}/monthly_aws_cost_report.zip"

  role             = "${data.terraform_remote_state.core.lambda_report_role}" 
  source_code_hash = "${base64sha256(file("${path.module}/monthly_aws_cost_report.zip"))}"
  handler          = "monthly_aws_cost_report.lambda_handler"
  runtime          = "python2.7"

  description = "Lists all the cost centre/quadrant for EC2 and RDS - emails and uploads to S3 - Updated ${var.ses_user}"

  memory_size = 128
  timeout     = 300

  environment {
    variables = {
      foo = "bar"
    }
  }
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "monthly_aws_cost_report_target" {
  target_id = "monthly_aws_cost_report"
  arn = "${aws_lambda_function.monthly_aws_cost_report.arn}"
  rule = "${var.cloudwatch_rule}"
}