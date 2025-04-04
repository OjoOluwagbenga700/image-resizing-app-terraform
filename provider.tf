terraform {
  required_version = "~> 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.25.0"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}


# Configure the AWS Provider
provider "aws" {
  region = var.region
}
# Configure the Docker Provider
provider "docker" {
  registry_auth {

    address  = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com"
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password

  }
}