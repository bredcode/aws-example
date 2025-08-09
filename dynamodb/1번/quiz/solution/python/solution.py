import boto3
import uuid
import time
from decimal import Decimal
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
    aws_secret_access_key="test"
)

# 테이블 조회
table = dynamodb.Table(TABLE_NAME)

# 전체 스캔
items = table.scan()["Items"]

print(f"\n📦 전체 데이터 ({len(items)}건):")
for i, it in enumerate(items, 1):
    print(f"{i}. {it['Name']} ({int(it['Age'])})")

# Age 오름차순 정렬 → 7번째(인덱스 6) 이름 확인
sorted_items = sorted(items, key=lambda x: x["Age"])
print(f"\n🔎 7번째 사람 이름: {sorted_items[6]['Name']}")
