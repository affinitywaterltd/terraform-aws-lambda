### Monthly report

resource "aws_lambda_function" "monthly_report" {
  function_name    = "Monthly_AWS_Report"
  filename         = "monthly_report.lambda"
  role             = "${data.terraform_remote_state.core.lambda_reporting_role.arn}"
  source_code_hash = "${base64sha256(file("${path.module}/monthly_report.lambda"))}"
  handler          = "lambda_handler"
  runtime          = "python2.7"

  description = "Lists all the cost centre/quadrant for EC2 and RDS - emails and uploads to S3"

  memory_size = 128
  timeout     = 300

  environment {
    variables = {
      foo = "bar"
    }
  }
}
