#!/bin/bash
set -e

apt-get update -qq
apt-get install -y -qq zip

echo "🚀 Packaging Lambda..."
cd /lambda
zip -r /tmp/lambda.zip .

echo "📡 Creating Lambda function..."
awslocal lambda create-function \
  --function-name my-lambda \
  --runtime nodejs18.x \
  --handler index.handler \
  --zip-file fileb:///tmp/lambda.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

echo "🌐 Creating API Gateway..."
rest_api_id=$(awslocal apigateway create-rest-api \
  --name my-api \
  --query 'id' --output text)

parent_id=$(awslocal apigateway get-resources \
  --rest-api-id $rest_api_id \
  --query 'items[?path==`"/"`].id' --output text)

# --- 루트(/)에 대한 GET (선택 사항)
awslocal apigateway put-method \
  --rest-api-id $rest_api_id \
  --resource-id $parent_id \
  --http-method GET \
  --authorization-type "NONE"

awslocal apigateway put-integration \
  --rest-api-id $rest_api_id \
  --resource-id $parent_id \
  --http-method GET \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:my-lambda/invocations

proxy_id=$(awslocal apigateway create-resource \
  --rest-api-id $rest_api_id \
  --parent-id $parent_id \
  --path-part "{proxy+}" \
  --query 'id' --output text)

awslocal apigateway put-method \
  --rest-api-id $rest_api_id \
  --resource-id $proxy_id \
  --http-method ANY \
  --authorization-type "NONE"

# --- 3. Lambda 프록시 통합
awslocal apigateway put-integration \
  --rest-api-id $rest_api_id \
  --resource-id $proxy_id \
  --http-method ANY \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:my-lambda/invocations

# --- Lambda 권한 허용
awslocal lambda add-permission \
  --function-name my-lambda \
  --statement-id apigateway-test \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn arn:aws:execute-api:us-east-1:000000000000:$rest_api_id/*/*/*

# --- API Gateway 배포
awslocal apigateway create-deployment \
  --rest-api-id $rest_api_id \
  --stage-name local

# --- 출력
echo ""
echo "✅ Test your API:"
echo "http://localhost:4566/restapis/${rest_api_id}/local/_user_request_/"
