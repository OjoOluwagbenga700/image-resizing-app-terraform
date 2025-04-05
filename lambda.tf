
resource "aws_lambda_function" "lambda_function" {
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.ecr_repo.repository_url}:latest"
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  timeout       = 30
  memory_size   = 1024


  environment {
    variables = {
      "SNS_TOPIC_ARN"      = aws_sns_topic.sns_alerts.arn
      "SOURCE_BUCKET"      = aws_s3_bucket.source_bucket.bucket
      "DESTINATION_BUCKET" = aws_s3_bucket.destination_bucket.bucket
      "TARGET_WIDTH"       = var.target_width
      "TARGET_HEIGHT"      = var.target_height

    }
  }
  depends_on = [docker_registry_image.image, aws_iam_role.lambda_role, aws_iam_role_policy_attachment.lambda_policy_attach]

}
