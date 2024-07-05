
provider "aws" {
  region = "us-east-1" # Change this to your desired region
}

module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.0"

  function_name = "inventory_lambda"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  source_path   = "${path.module}/lambda"

  attach_policy_arn = [
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/CloudWatchFullAccess",
    "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
  ]

  tags = {
    Terraform = "true"
    Environment = "dev"
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda.this_lambda_function_name
  principal     = "events.amazonaws.com"
}
