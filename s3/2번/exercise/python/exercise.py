import boto3
from pathlib import Path

# LocalStack에서 사용하는 endpoint 및 region
LOCALSTACK_ENDPOINT = "https://a45f-61-43-16-236.ngrok-free.app"
AWS_REGION         = "us-east-1"

# boto3 클라이언트 생성
s3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# 버킷 및 관련 내용 정의
bucket_name   = "my-bucket"          # 이미 만들어 둔 버킷
local_upload  = Path("../dog.jpg")   # 업로드할 원본 이미지
s3_key        = "images/dog.jpg"  # S3 안에서의 경로(Key)
local_target  = Path("downloaded_dog.jpg")  # 내려받을 파일 이름

# 이미지 업로드
# 작은 파일은 put_object, 큰 파일은 upload_file 를 주로 사용
s3.upload_file(Filename=str(local_upload), Bucket=bucket_name, Key=s3_key)
print(f"✅ 업로드 완료: {local_upload}  ➜  s3://{bucket_name}/{s3_key}")

# 버킷 안의 객체 확인
objects = s3.list_objects_v2(Bucket=bucket_name, Prefix="images/")
print("📂 S3 images/ 폴더 내용:")
for o in objects.get("Contents", []):
    print("  -", o["Key"])

# 이미지 다운로드 (파일 저장)
s3.download_file(
    Bucket=bucket_name,
    Key=s3_key,
    Filename=str(local_target)   # 여기에 실제로 파일이 생깁니다
)
print(f"📥 다운로드 완료: s3://{bucket_name}/{s3_key}  ➜  {local_target}")