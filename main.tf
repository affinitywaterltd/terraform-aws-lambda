### Monthly report

resource "aws_lambda_function" "monthly_report" {
  function_name = "Monthly_AWS_Report"
  filename      = "${path.module}/monthly_report.zip"

  role             = "${data.terraform_remote_state.core.lambda_reporting_role.arn}"
  #role             = "arn:aws:iam::986618351900:role/Lambda_Reporting"
  source_code_hash = "${base64sha256(file("${path.module}/monthly_report.zip"))}"
  handler          = "monthly_report.lambda_handler"
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

