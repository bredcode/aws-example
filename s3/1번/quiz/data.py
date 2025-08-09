import boto3

# LocalStack 설정
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
DATA_KEY = "problem.txt"

s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

bucket_name = "my-bucket"

# 📜 이환천 - 체중계2
poem = """체중계2 - 이환천
외제차도
아니면서

밟는만큼
잘나가네
"""

# S3에 업로드
s3.put_object(Bucket=bucket_name, Key=DATA_KEY, Body=poem)

# 업로드된 파일 다시 가져오기
response = s3.get_object(Bucket=bucket_name, Key=DATA_KEY)
body = response['Body'].read().decode('utf-8')

print(f"📄 Content of {DATA_KEY}:")
print(body)
