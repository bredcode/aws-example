import boto3
import time
from botocore.exceptions import ClientError

# LocalStack 설정
ENDPOINT    = "http://localhost:4566"
REGION      = "us-east-1"
TABLE_NAME  = "Users"

# 클라이언트 생성
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

# 기존 테이블이 있으면 삭제
try:
    table = dynamodb.Table(TABLE_NAME)
    table.load()                                 # 존재 여부 확인
    print(f"⚠️  Table '{TABLE_NAME}' already exists. Deleting…")
    table.delete()
    while True:                                  # 삭제 완료 대기
        try:
            table.load()
            time.sleep(0.3)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                break
            raise
    print(f"🗑️  Deleted table: {TABLE_NAME}")
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceNotFoundException":
        print(f"✅ Table '{TABLE_NAME}' does not exist, no need to delete.")
    else:
        raise

# 테이블 새로 생성 (PK = UserId)
table = dynamodb.create_table(
    TableName=TABLE_NAME,
    AttributeDefinitions=[
        {"AttributeName": "UserId", "AttributeType": "S"},
    ],
    KeySchema=[
        {"AttributeName": "UserId", "KeyType": "HASH"},
    ],
    BillingMode="PAY_PER_REQUEST",
)
table.wait_until_exists()
print(f"✅ Created table: {TABLE_NAME}")

# 현재 존재하는 테이블 목록 출력
print("📂 Tables in LocalStack DynamoDB:")
for t in dynamodb.tables.all():
    print(f" - {t.name}")
