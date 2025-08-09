import boto3
import botocore

# LocalStack 설정
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
queue_name = "my-queue"

# SQS 클라이언트 생성
sqs = boto3.client(
    "sqs",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# 기존 큐가 존재하는 경우 삭제
try:
    response = sqs.get_queue_url(QueueName=queue_name)
    queue_url = response["QueueUrl"]
    print(f"⚠️  Queue '{queue_name}' already exists. Deleting...")

    sqs.delete_queue(QueueUrl=queue_url)
    print(f"🗑️  Deleted queue: {queue_name}")

except botocore.exceptions.ClientError as e:
    if e.response["Error"]["Code"] == "AWS.SimpleQueueService.NonExistentQueue":
        print(f"✅ Queue '{queue_name}' does not exist, no need to delete.")
    else:
        raise e

# 새 큐 생성
try:
    response = sqs.create_queue(QueueName=queue_name)
    print(f"✅ Created queue: {queue_name}")
except Exception as e:
    print(f"❌ Error creating queue: {e}")

# 전체 큐 목록 조회 (LocalStack에서는 QueueUrls로 확인 가능)
print("📂 Queues in LocalStack:")
queues = sqs.list_queues().get("QueueUrls", [])
for url in queues:
    print(f" - {url}")
