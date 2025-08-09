import boto3
import uuid
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import random

ENDPOINT = "http://localhost:4566"
REGION   = "us-east-1"
TABLE    = "Users" # Dept (파티션 키) + Age (정렬 키)

# 1. 클라이언트 생성
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

# 2. Table 객체 생성
table = dynamodb.Table(TABLE)

# 첫 번째 아이템  (PK = Dept='HR' ,  SK = Age)
dept = "HR"               # 파티션 키
age  = Decimal(random.randint(0, 99))        # 정렬 키
emp  = str(uuid.uuid4())  # 부가 정보: EmployeeId

table.put_item(
    Item={
        "Dept": dept,
        "Age":  age,
        "EmpId": emp,
        "Name": "Alice",
    }
)
print("🆕 CREATE →", dept, age)

# 두 번째 아이템  (Dept='HR', Age = 20)
dept = "HR"
age  = Decimal(random.randint(0, 99))
emp  = str(uuid.uuid4())

table.put_item(
    Item={
        "Dept": dept,
        "Age":  age,
        "EmpId": emp,
        "Name": "Dave",
    }
)
print("🆕 CREATE →", dept, age)

# FULL SCAN
response = table.scan()
items = response.get("Items", [])

print(f"📦 전체 데이터 ({len(items)}건):")
for i, item in enumerate(items, 1):
    print(f"{i}. {item}")

# Dept='HR' 기준 Age 오름차순 Query
query_result = table.query(
    KeyConditionExpression=Key("Dept").eq("HR"),
    ScanIndexForward=True # ASC(오름차순)
)

print("\n📑 Query: Dept='HR'  Age 오름차순")
for idx, item in enumerate(query_result["Items"]):
    print(f"{idx}. {item['Name']}  -  Age: {int(item['Age'])}")

