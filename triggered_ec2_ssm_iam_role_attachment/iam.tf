
#
# SSM Role attachment
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

resource "aws_iam_role" "lambda_ec2_ssm_iam_role" {
  name = "lambda_ec2_ssm_iam_role"

  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_policy" "lambda_ec2_ssm_iam_policy" {
  name   = "lambda_ec2_ssm_iam_policy"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:AssociateIamInstanceProfile"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:instance-profile/ssm_role"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_ec2_ssm_iam_policy_attach" {
  role       = aws_iam_role.lambda_ec2_ssm_iam_role.name
  policy_arn = aws_iam_policy.lambda_ec2_ssm_iam_policy.arn
}


resource "aws_iam_role_policy_attachment" "lambda_ec2_ssm_iam_policy_execution_attach" {
  role       = aws_iam_role.lambda_ec2_ssm_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
