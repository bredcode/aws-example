import boto3

# LocalStack 설정
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
bucket_name = "my-bucket"
file_key = "problem.txt"

# boto3 S3 클라이언트 생성
s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# S3 객체 가져오기
response = s3.get_object(Bucket=bucket_name, Key=file_key)

# Body (스트림) → 문자열로 변환
content = response["Body"].read().decode("utf-8")

print(f"📄 Content of {file_key}:\n{content}")
