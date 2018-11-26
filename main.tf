### Monthly report

resource "aws_lambda_function" "monthly_report" {
  function_name = "Monthly_AWS_Report"
  filename      = "${path.module}/monthly_report.zip"

  #Couldnt get working referencing the role from the module output, added by static name instead
  #role             = "${data.terraform_remote_state.core.lambda_report_role}" 
  role             = "Lambda_Reporting"
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

