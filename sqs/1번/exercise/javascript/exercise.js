// sqs_producer_consumer.mjs
import {
  SQSClient,
  GetQueueUrlCommand,
  SendMessageCommand,
  ReceiveMessageCommand,
  DeleteMessageCommand,
} from "@aws-sdk/client-sqs";

// LocalStack 환경 설정
const LOCALSTACK_ENDPOINT = "http://localhost:4566";
const AWS_REGION = "us-east-1";
const QUEUE_NAME = "my-queue";

// SQS 클라이언트
const sqs = new SQSClient({
  region: AWS_REGION,
  endpoint: LOCALSTACK_ENDPOINT,
  credentials: {
    accessKeyId: "test",
    secretAccessKey: "test",
  },
});

// 큐 URL 가져오기
async function getQueueUrl() {
  const { QueueUrl } = await sqs.send(new GetQueueUrlCommand({ QueueName: QUEUE_NAME }));
  return QueueUrl;
}

// 1) 프로듀서: 메시지 발송
async function sendMessages(queueUrl, n = 10) {
  /* n개의 메시지를 큐로 발송 */
  for (let i = 0; i < n; i++) {
    const body = `Message-${String(i).padStart(3, "0")}`;
    const { MessageId } = await sqs.send(
      new SendMessageCommand({
        QueueUrl: queueUrl,
        MessageBody: body,
        // 표준 큐에서는 아래 속성들로 순서를 직접 제어할 수 없음
        // FIFO 큐라면 MessageGroupId, MessageDeduplicationId 필요
      })
    );
    console.log(`➡️  Sent: ${body} (MessageId=${MessageId})`);
  }
}

// 2) 컨슈머: 메시지 수신·삭제
async function receiveAndDelete(queueUrl) {
  /*
    한 번 폴링으로 메시지 수신 후 처리·삭제
    (필요 시 반복 호출하거나 루프 구성 가능)
  */
  const { Messages: messages = [] } = await sqs.send(
    new ReceiveMessageCommand({
      QueueUrl: queueUrl,
      MaxNumberOfMessages: 10, // 한 번에 최대 10개
      WaitTimeSeconds: 2, // Long‑poll (2초)
      VisibilityTimeout: 5, // 처리 시간 마련
    })
  );

  for (const msg of messages) {
    // 실질적인 작업을 여기서 수행
    console.log(`⬅️  Received: ${msg.Body} (MessageId=${msg.MessageId})`);

    // 처리 후 삭제
    await sqs.send(
      new DeleteMessageCommand({
        QueueUrl: queueUrl,
        ReceiptHandle: msg.ReceiptHandle,
      })
    );
    console.log(` 🗑️  Deleted: ${msg.Body}`);
  }
}

// 메인 실행
async function main() {
  const queueUrl = await getQueueUrl();
  await sendMessages(queueUrl, 10); // 10개 발송
  await receiveAndDelete(queueUrl); // 수신·삭제
}

main().catch((err) => console.error("❌ Error:", err));
