output "cloudfront_domain" {
  value = aws_cloudfront_distribution.cdn.domain_name
}

output "lambda_function_url" {
  value = aws_lambda_function_url.visitor_url.function_url
}

output "s3_bucket_name" {
  value = aws_s3_bucket.site.bucket
}
