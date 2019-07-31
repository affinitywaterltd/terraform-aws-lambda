
variable "cloudwatch_rule_name" {}
variable "cloudwatch_rule_arn" {}

### Update Maintenance Window Parameters

resource "aws_lambda_function" "triggered_ec2_tagging_citrix_mcs_servers" {
  function_name = "triggered_ec2_tagging_citrix_mcs_servers"
  filename      = "${path.module}/triggered_ec2_tagging_citrix_mcs_servers.zip"

  role             = "${data.terraform_remote_state.core.lambda_ec2_tagging_citrix_mcs_servers_role}" 
  source_code_hash = "${base64sha256(file("${path.module}/triggered_ec2_tagging_citrix_mcs_servers.zip"))}"
  handler          = "triggered_ec2_tagging_citrix_mcs_servers.lambda_handler"
  runtime          = "python3.7"

  description = "Add default tags to servers created by Citrix Machine Creation Services (MCS)"

  tags = "${local.base_tags}"

  memory_size = 128
  timeout     = 30

  environment {
    variables = {
      account = "${var.account}",
      environment = "${var.environment}"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.triggered_ec2_tagging_citrix_mcs_servers.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${var.cloudwatch_rule_arn}"
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "triggered_ec2_tagging_citrix_mcs_servers" {
  target_id = "triggered_ec2_tagging_citrix_mcs_servers"
  arn = "${aws_lambda_function.triggered_ec2_tagging_citrix_mcs_servers.arn}"
  rule = "${var.cloudwatch_rule_name}"
}
