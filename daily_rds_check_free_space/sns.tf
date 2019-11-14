resource "aws_sns_topic" "sns_alerts_dba_info" {
  name = "sns_alerts_dba_info"
  display_name = "RDS-Info"
}

resource "aws_sns_topic" "sns_alerts_dba_warning" {
  name = "sns_alerts_dba_warning"
  display_name = "RDS-Warn"
}