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

# 기존 테이블이 있으면 삭제
try:
    table = dynamodb.Table(TABLE_NAME)
    table.load()                        # 존재 여부 체크
    print(f"⚠️  Table '{TABLE_NAME}' already exists. Deleting…")
    table.delete()
    # 삭제 완료 대기
    while True:
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

# 테이블 새로 생성
table = dynamodb.create_table(
    TableName=TABLE_NAME,
    AttributeDefinitions=[{"AttributeName": "UserId", "AttributeType": "S"}],
    KeySchema=[{"AttributeName": "UserId", "KeyType": "HASH"}],
    BillingMode="PAY_PER_REQUEST"
)
table.wait_until_exists()
print(f"✅ Created table: {TABLE_NAME}")

# 10개 샘플 데이터 삽입
people = [
    ("Alice",   24),
    ("Bob",     28),
    ("Charlie", 19),
    ("Diana",   31),
    ("Eve",     27),
    ("Frank",   33),
    ("Grace",   26),
    ("Heidi",   29),
    ("Ivan",    22),
    ("Judy",    25),
]

for name, age in people:
    user_id = str(uuid.uuid4())
    table.put_item(
        Item={
            "UserId": user_id,
            "Name":   name,
            "Age":    Decimal(age)      # 숫자는 Decimal로!
        }
    )
    print(f"🆕 Inserted → {name} ({age})  [UserId={user_id}]")

print("✅ 총 10개 레코드 삽입 완료.")

# 전체 스캔
items = table.scan()["Items"]

print(f"\n📦 전체 데이터 ({len(items)}건):")
for i, it in enumerate(items, 1):
    print(f"{i}. {it['Name']} ({int(it['Age'])})")

# Age 오름차순 정렬 → 7번째(인덱스 6) 이름 확인
sorted_items = sorted(items, key=lambda x: x["Age"])
print(f"\n🔎 7번째 사람 이름: {sorted_items[6]['Name']}")
