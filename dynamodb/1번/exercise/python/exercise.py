import boto3
import uuid
from decimal import Decimal

ENDPOINT = "http://localhost:4566"
REGION   = "us-east-1"
TABLE    = "Users"

# 1. 클라이언트 생성
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# 2. Table 객체 생성
table = dynamodb.Table(TABLE)

# CREATE
userId = str(uuid.uuid4())
table.put_item(
    Item={
        "UserId": userId,
        "Name": "Alice",
        "Age": Decimal(29),
        "Item": {
            "ProductId": "P‑100",
            "Price": Decimal("19.99")
        }
    }
)
print("🆕 CREATE →", userId)

# READ
res = table.get_item(
    Key={"UserId": userId}
)
Item = res.get("Item")
print("📄 READ:", Item)

# CREATE
userId = str(uuid.uuid4())
table.put_item(
    Item={
        "UserId": userId,
        "Name": "Dave",
        "Age": Decimal(20)
    }
)
print("🆕 CREATE →", userId)

# READ
res = table.get_item(
    Key={"UserId": userId}
)
Item = res.get("Item")
print("📄 READ:", Item)

# UPDATE
table.update_item(
    Key={"UserId": userId},
    UpdateExpression="SET #n = :name, #a = :age",
    ExpressionAttributeNames={
        "#n": "Name",
        "#a": "Age"
    },
    ExpressionAttributeValues={
        ":name": "Bob",
        ":age": Decimal(30)
    }
)
print("✏️  UPDATE")

# FULL SCAN
response = table.scan(
    TableName=TABLE
)

items = response.get("Items", [])

print(f"📦 전체 데이터 ({len(items)}건):")
for i, item in enumerate(items, 1):
    print(f"{i}. {item}")


# DELETE
table.delete_item(
    Key={"UserId": userId}
)
print("❌ DELETE")
