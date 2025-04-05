
# Create an SNS topic for sending alerts
resource "aws_sns_topic" "sns_alerts" {
  name = var.sns_topic_name
}


# Create an email subscription for the SNS topic
resource "aws_sns_topic_subscription" "sns_alerts_sub" {
  topic_arn = aws_sns_topic.sns_alerts.arn
  protocol  = "email"
  endpoint  = var.email_endpoint

}

  