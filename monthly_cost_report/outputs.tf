
output "monthly_cost_report"
{
    value = "${aws_lambda_function.monthly_cost_report.arn}"
}