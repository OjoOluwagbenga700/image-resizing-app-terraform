# image-resizing-app-terraform
Delivering optimized images across various devices is crucial for modern applications. While AWS Lambda offers a serverless compute environment, its standard runtimes can sometimes limit the choice of image processing tools. This article explores a powerful solution: leveraging Dockerized container images stored in Amazon ECR and deployed via Lambda. 
By packaging libraries like Sharp or Pillow into custom containers, we gain unparalleled flexibility in building a serverless image resizing application triggered by Amazon S3, offering a scalable and efficient way to manage your visual assets.


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/uzrnkkl4lz1xq7mx9kf6.png)



Requirements
[Create an AWS account]
[AWS CLI] installed and configured
[Git Installed]
[Terraform Installed]
Deployment Instructions

Create a new directory, navigate to that directory in a terminal and clone the GitHub repository:

git clone https://github.com/OjoOluwagbenga700/image-resizing-app-terraform.git

Change directory to the pattern directory:

cd image-resizing-app-terraform
From the command line, run:

```
terraform init
```

From the command line, run:

```
terraform plan
```

From the command line, run:

```
terraform apply --auto-approve
```

Testing
Confirm all resources are deployed on the AWS console. navigate to the source bucket created and upload and image. immediately, the lambda function is triggered to resize the the image and upload the new file in the destination bucket.

Cleanup
To delete the resources, run:

```
terraform destroy --auto-approve
```
