import boto3

# LocalStack에서 사용하는 endpoint 및 region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"

# boto3 클라이언트 생성
s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",  # LocalStack에서는 아무 값이나 사용 가능
    aws_secret_access_key="test"
)

# 버킷 이름 정의
bucket_name = "my-bucket"

# 테스트용 파일 업로드
s3.put_object(Bucket=bucket_name, Key="py_test.txt", Body="Hello, LocalStack With Python!")

# 생성된 버킷 목록 출력
response = s3.list_buckets()
print("📂 Buckets in LocalStack:")
for bucket in response['Buckets']:
    print(f" - {bucket['Name']}")

# 업로드된 객체 목록 확인
objects = s3.list_objects_v2(Bucket=bucket_name)
print("📂 Files in my-bucket:")
for obj in objects.get("Contents", []):
    print(f" - {obj['Key']}")

# test.txt 오브젝트 가져오기
response = s3.get_object(Bucket=bucket_name, Key="py_test.txt")

# 본문(body)을 바이트 스트림으로 가져와서 디코딩
body = response['Body'].read().decode('utf-8')

print("📄 Content of test.txt:")
print(body)

# 객체 삭제
s3.delete_object(Bucket=bucket_name, Key="py_test.txt")
print("🗑️  Deleted object: py_test.txt")

# 업로드된 객체 목록 확인
objects = s3.list_objects_v2(Bucket=bucket_name)
print("📂 Files in my-bucket:")
for obj in objects.get("Contents", []):
    print(f" - {obj['Key']}")
