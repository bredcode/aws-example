import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, ScanCommand } from "@aws-sdk/lib-dynamodb";

// LocalStack 설정
const ENDPOINT = "http://localhost:4566";
const REGION = "us-east-1";
const TABLE_NAME = "Users";

// 클라이언트 생성 (Document 버전 → 타입 자동 변환)
const ddbClient = new DynamoDBClient({
  endpoint: ENDPOINT,
  region: REGION,
  credentials: { accessKeyId: "test", secretAccessKey: "test" },
});
const docClient = DynamoDBDocumentClient.from(ddbClient);

// 전체 스캔
const scanRes = await docClient.send(new ScanCommand({ TableName: TABLE_NAME }));
const items = scanRes.Items ?? [];

console.log(`\n📦 전체 데이터 (${items.length}건):`);
items.forEach((it, idx) => {
  console.log(`${idx + 1}. ${it.Name} (${it.Age})`);
});

// Age 오름차순 정렬 → 7번째(인덱스 6) 이름 확인
const sortedItems = items.sort((a, b) => a.Age - b.Age);

if (sortedItems.length >= 7) {
  console.log(`\n🔎 7번째 사람 이름: ${sortedItems[6].Name}`);
} else {
  console.log("\n⚠️ 데이터가 7개 미만입니다.");
}
