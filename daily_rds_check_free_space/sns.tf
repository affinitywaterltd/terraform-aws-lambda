resource "aws_sns_topic" "sns_alerts_dba_info" {
  name = "sns_alerts_dba_info"
  display_name = "RDS-Info"
}

resource "aws_sns_topic" "sns_alerts_dba_warning" {
  name = "sns_alerts_dba_warning"
  display_name = "RDS-Warn"
}



resource "aws_sns_topic_subscription" "sns-topic-info" {
  count     = "${length(var.sns_sms_list)}"
  provider  = "aws.sns2sms"
  topic_arn = "${aws_sns_topic.sns_alerts_dba_info.arn}"
  protocol  = "sms"
  endpoint  = "${var.sns_sms_list.["info"]}"
}