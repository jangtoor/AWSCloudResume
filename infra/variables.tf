variable "project_name" {
  type    = string
  default = "aws-cloud-resume"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "domain_name" {
  type = string
  # example: "jangtoor.com"
}

variable "create_www_record" {
  type    = bool
  default = true
}

variable "hosted_zone_id" {
  type = string
  # Route53 Hosted Zone ID for jangtoor.com
}

variable "s3_bucket_name" {
  type = string
  # example: "jang-cloud-resume-challenge"
}

variable "dynamodb_table_name" {
  type    = string
  default = "cloudresume"
}

variable "lambda_function_name" {
  type    = string
  default = "Lambda_Cloudresumefunction"
}

variable "item_id" {
  type    = string
  default = "visitors"
}
