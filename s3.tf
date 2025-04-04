resource "aws_s3_bucket" "source_bucket" {
  bucket = var.source_bucket_name
  tags = {
    Name = var.source_bucket_name
  }
  lifecycle {
    prevent_destroy =false
  }

}
resource "aws_s3_bucket" "destination_bucket" {
  bucket = var.destination_bucket_name
  tags = {
    Name = var.destination_bucket_name
  }
  lifecycle {
    prevent_destroy = false
  }

}
resource "aws_s3_bucket_notification" "source_bucket_notification" {
  bucket = aws_s3_bucket.source_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_function.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [aws_lambda_permission.allow_s3]
}

