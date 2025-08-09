import boto3
import uuid
import time
from decimal import Decimal
from boto3.dynamodb.conditions import Key
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
    table.load()  # 존재 여부 확인
    print(f"⚠️  Table '{TABLE_NAME}' already exists. Deleting…")
    table.delete()
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

# 테이블 새로 생성 (PK = Dept, SK = Age)
table = dynamodb.create_table(
    TableName=TABLE_NAME,
    AttributeDefinitions=[
        {"AttributeName": "Dept", "AttributeType": "S"},  # 파티션 키
        {"AttributeName": "Age", "AttributeType": "N"},   # 정렬 키
    ],
    KeySchema=[
        {"AttributeName": "Dept", "KeyType": "HASH"},
        {"AttributeName": "Age",  "KeyType": "RANGE"},
    ],
    BillingMode="PAY_PER_REQUEST",
)
table.wait_until_exists()
print(f"✅ Created table with composite key (Dept + Age): {TABLE_NAME}")

# 샘플 데이터 삽입
people = [
    ("HR",  "Alice",  24),
    ("SALES",  "Bob",  28),
    ("HR",  "Charlie",  19),
    ("SALES",  "Diana",  31),
    ("HR",  "Eve",  27),
    ("HR",  "Frank",  33),
    ("HR",  "Grace",  26),
    ("SALES",  "Heidi",  29),
    ("HR",  "Ivan",  22),
    ("HR",  "Judy",  25),
]

for dept, name, age in people:
    emp_id = str(uuid.uuid4())
    table.put_item(
        Item={
            "Dept":  dept,              # PK
            "Age":   Decimal(age),      # SK
            "EmpId": emp_id,
            "Name":  name
        }
    )
    print(f"🆕 Inserted → {dept} {name} ({age})  [EmpId={emp_id}]")

print("✅ 총 10개 레코드 삽입 완료.")

# Dept='HR' 기준 Age 오름차순 Query
query_result = table.query(
    KeyConditionExpression=Key("Dept").eq("HR"),
    ScanIndexForward=True # ASC(오름차순)
)

print("\n📑 Query: Dept='HR'  Age 오름차순")
for idx, item in enumerate(query_result["Items"]):
    print(f"{idx}. {item['Name']}  -  Age: {int(item['Age'])}")

items_hr = query_result["Items"]          # 정렬된 리스트
if len(items_hr) >= 3:
    third_person = items_hr[2]            # 0,1,2 → 세 번째
    print(f"\n🔎 HR 부서 세 번째 사람: {third_person['Name']}  (Age: {int(third_person['Age'])})")
else:
    print("\n⚠️ HR 부서에 세 명 미만의 레코드만 존재합니다.")