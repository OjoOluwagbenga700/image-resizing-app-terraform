# image-resizing-app-terraform

Building responsive and event-driven applications is a hallmark of modern cloud development. This project creates a serverless image resizing workflow powered by Amazon S3, AWS Lambda (using Docker containers from ECR), and Amazon SNS. Upon image upload to S3, SNS notifications will signal the start of the resizing process within Lambda, and further notifications will confirm successful completion. This event-driven architecture ensures timely processing and keeps you informed every step of the way, leading to efficient image optimization.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/uzrnkkl4lz1xq7mx9kf6.png)



**Requirements**
 An AWS account
 AWS CLI installed and configured
 Git Installed
 Terraform Installed

**Deployment Instructions**

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

**Testing**

Confirm all resources are deployed on the AWS console. navigate to the source bucket created and upload and image. immediately, the lambda function is triggered to resize the the image and upload the new file in the destination bucket.

Cleanup
To delete the resources, run:

```
terraform destroy --auto-approve
```
