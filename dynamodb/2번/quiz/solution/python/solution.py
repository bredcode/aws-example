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