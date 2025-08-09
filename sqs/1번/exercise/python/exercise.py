import boto3
import time

# LocalStack 환경 설정
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
QUEUE_NAME = "my-queue"

# SQS 클라이언트
sqs = boto3.client(
    "sqs",
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

# 큐 URL 가져오기
queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]

# 1) 프로듀서: 메시지 발송
def send_messages(n: int = 10):
    # n개의 메시지를 큐로 발송
    for i in range(n):
        body = f"Message-{i:03d}"
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=body,
            # 표준 큐에서는 아래 속성들로 순서를 직접 제어할 수 없음
            # FIFO 큐라면 MessageGroupId, MessageDeduplicationId 필요
        )
        print(f"➡️  Sent: {body} (MessageId={response['MessageId']})")

# 2) 컨슈머: 메시지 수신·삭제
def receive_and_delete():
    """
    최대 max_batches번까지 폴링하며 메시지 수신.
    메시지를 처리한 뒤 반드시 DeleteMessage로 삭제.
    """
    messages = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,   # 한 번에 최대 10개
        WaitTimeSeconds=2,        # Long‑poll (2초)
        VisibilityTimeout=5,      # 처리 시간 마련
    ).get("Messages", [])

    
    for msg in messages:
        # 실질적인 작업을 여기서 수행
        print(f"⬅️  Received: {msg['Body']} (MessageId={msg['MessageId']})")

        # 처리 후 삭제
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg["ReceiptHandle"],
        )
        print(f" 🗑️  Deleted: {msg['Body']}")

if __name__ == "__main__":
    send_messages(10)          # 10개 발송
    receive_and_delete()       # 수신·삭제
