# Create ECR Repository
resource "aws_ecr_repository" "ecr_repo" {
  name                 = var.repository_name
  image_tag_mutability = "MUTABLE"
}

# Create Docker image
resource "docker_image" "image" {
  name = "${aws_ecr_repository.ecr_repo.repository_url}:latest"
  build {
    context    = "${path.module}/src"
    dockerfile = "Dockerfile"
    
  }
  depends_on = [ aws_ecr_repository.ecr_repo ]
}
# Push docker image to ECR repo
resource "docker_registry_image" "image" {
  name = docker_image.image.name
depends_on = [ docker_image.image ]
}