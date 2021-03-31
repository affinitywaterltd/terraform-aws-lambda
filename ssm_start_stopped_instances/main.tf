### Update Maintenance Window Parameters

resource "aws_lambda_function" "ssm_start_stopped_instances" {
  function_name = "SSM_start_stopped_instances"
  filename      = "${path.module}/ssm_start_stopped_instances.zip"

  role = aws_iam_role.lambda_ssm_start_stopped_instances_iam_role.arn
  source_code_hash = filebase64sha256(
    "${path.module}/ssm_start_stopped_instances.zip",
  )
  handler = "ssm_start_stopped_instances.lambda_handler"
  runtime = "python3.8"

  description = "Identofy EC2 instances tagged for the active Maintenance window and start stopped instances"

  tags = local.base_tags

  memory_size = 128
  timeout     = 30
}