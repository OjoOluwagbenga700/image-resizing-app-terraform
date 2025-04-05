variable "region" {
  description = "The AWS region to deploy the resources in."
  type        = string
  default     = "us-east-1"

}

variable "source_bucket_name" {
  description = "The name of the source S3 bucket."
  type        = string
  default     = "imagethumbnail007"

}

variable "destination_bucket_name" {
  description = "The name of the destination S3 bucket."
  type        = string
  default     = "imagethumbnail007-resized"

}
variable "email_endpoint" {
  description = "The name of the destination S3 bucket."
  type        = string
  default     = "ojosamuel700@gmail.com"


}

variable "function_name" {
  description = "The name of the Lambda function."
  type        = string
  default     = "image_lambda_function"

}

variable "sns_topic_name" {
  description = "The name of the SNS topic."
  type        = string
  default     = "image-processing-alerts"

}

variable "repository_name" {
  description = "The name of the ECR repository."
  type        = string
  default     = "image-processing-repo"

}



