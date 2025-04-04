
resource "aws_lambda_function" "lambda_function" {
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.ecr_repo.repository_url}:latest"
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn


  environment {
    variables = {
      "SNS_TOPIC_ARN" = aws_sns_topic.sns_alerts.arn

    }
  }
  depends_on = [docker_registry_image.image, aws_iam_role.lambda_role, aws_iam_role_policy_attachment.lambda_policy_attach]

}
