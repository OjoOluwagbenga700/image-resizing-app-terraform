# Define the trust relationship for lambda


data "aws_iam_policy_document" "lambda_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Create the lambda role
resource "aws_iam_role" "lambda_role" {
  name               = "image-resize-lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
}

# Define the lambda policy document
data "aws_iam_policy_document" "lambda_policy_doc" {
  statement {
    actions = ["sns:Publish"]
    effect  = "Allow"
    resources = [
      "arn:aws:sns:${var.region}:${data.aws_caller_identity.current.account_id}:${var.sns_topic_name}"
    ]
  }
  statement {
    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]
    effect  = "Allow"
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }
  statement {
    actions = ["s3:GetObject", "s3:PutObject", "s3:CreateBucket", "s3:ListBucket"]
    effect  = "Allow"
    resources = [
      "arn:aws:s3:::${var.source_bucket_name}",
      "arn:aws:s3:::${var.source_bucket_name}/*",
      "arn:aws:s3:::${var.destination_bucket_name}",
      "arn:aws:s3:::${var.destination_bucket_name}/*"

    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetAuthorizationToken"
    ]
    resources = [aws_ecr_repository.ecr_repo.arn]
  }
}


# Create the lambda  policy
resource "aws_iam_policy" "lambda_policy" {
  name   = "image-lambda-policy"
  policy = data.aws_iam_policy_document.lambda_policy_doc.json
}

# Attach the Lambda policy to the Lambda role 
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}



resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.source_bucket.arn
  depends_on    = [aws_lambda_function.lambda_function]
}

