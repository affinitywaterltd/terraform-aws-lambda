
#
# AWS Backups cleanup expired restore points
#
data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_aws_backup_cleanup_role" {
  name = "lambda-aws-backup-cleanup-role"

  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_snapshot_cleaup_policy_attach" {
  role       = aws_iam_role.lambda_aws_backup_cleanup_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSBackupFullAccess"
}

resource "aws_iam_policy" "lambda_cloudwatch_logs_writing_policy" {
  name   = "lambda-cloudwatch-logs-writing"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups",
                "logs:PutRetentionPolicy",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_backup_logging_policy_attach" {
  role       = aws_iam_role.lambda_aws_backup_cleanup_role.name
  policy_arn = aws_iam_policy.lambda_cloudwatch_logs_writing_policy.arn
}