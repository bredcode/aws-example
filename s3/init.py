import boto3
import botocore

# LocalStack 설정
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
bucket_name = "my-bucket"

# S3 클라이언트 생성
s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# 📌 기존 버킷이 존재하는 경우, 내부 객체까지 전부 삭제 후 버킷 제거
try:
    s3.head_bucket(Bucket=bucket_name)  # 버킷 존재 여부 확인
    print(f"⚠️  Bucket '{bucket_name}' already exists. Deleting...")

    # 버킷 내 모든 객체 삭제
    objects = s3.list_objects_v2(Bucket=bucket_name)
    for obj in objects.get("Contents", []):
        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
        print(f"🗑️  Deleted object: {obj['Key']}")

    # 버킷 삭제
    s3.delete_bucket(Bucket=bucket_name)
    print(f"🗑️  Deleted bucket: {bucket_name}")

except botocore.exceptions.ClientError as e:
    # 존재하지 않을 경우 (404)
    if e.response["Error"]["Code"] == "404":
        print(f"✅ Bucket '{bucket_name}' does not exist, no need to delete.")
    else:
        raise e

# ✅ 버킷 새로 생성
try:
    s3.create_bucket(Bucket=bucket_name)
    print(f"✅ Created bucket: {bucket_name}")
except Exception as e:
    print(f"❌ Error creating bucket: {e}")

# 버킷 목록 출력
response = s3.list_buckets()
print("📂 Buckets in LocalStack:")
for bucket in response["Buckets"]:
    print(f" - {bucket['Name']}")
