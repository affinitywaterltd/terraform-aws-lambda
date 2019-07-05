
variable "cloudwatch_rule_name" {}
variable "cloudwatch_rule_arn" {}

### Update Maintenance Window Parameters

resource "aws_lambda_function" "triggered_maintenance_window_parameter_injection" {
  function_name = "triggered_maintenance_window_parameter_injection"
  filename      = "${path.module}/triggered_maintenance_window_parameter_injection.zip"

  role             = "${data.terraform_remote_state.core.lambda_maintenance_window_update_role}" 
  source_code_hash = "${base64sha256(file("${path.module}/triggered_maintenance_window_parameter_injection.zip"))}"
  handler          = "triggered_maintenance_window_parameter_injection.lambda_handler"
  runtime          = "python3.7"

  description = "Updates task parameters to workaround Terraform limitation with Automation Tasks"

  tags = "${local.base_tags}"

  memory_size = 128
  timeout     = 3

  environment {
    variables = {
      task_name_filter = "start_stopped_instances"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.triggered_maintenance_window_parameter_injection.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${var.cloudwatch_rule_arn}"
}

# Attach Cloudwatch event to lambda function
resource "aws_cloudwatch_event_target" "triggered_maintenance_window_parameter_injection" {
  target_id = "triggered_maintenance_window_parameter_injection"
  arn = "${aws_lambda_function.triggered_maintenance_window_parameter_injection.arn}"
  rule = "${var.cloudwatch_rule_name}"
}
