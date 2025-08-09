import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, QueryCommand } from "@aws-sdk/lib-dynamodb";

// LocalStack 설정
const ENDPOINT = "http://localhost:4566";
const REGION = "us-east-1";
const TABLE = "Users"; // Dept (파티션 키) + Age (정렬 키)

// 1. 클라이언트 생성
const ddbClient = new DynamoDBClient({
  endpoint: ENDPOINT,
  region: REGION,
  credentials: { accessKeyId: "test", secretAccessKey: "test" },
});
const docClient = DynamoDBDocumentClient.from(ddbClient);

// Dept='HR' 기준 Age 오름차순 Query
const queryResult = await docClient.send(
  new QueryCommand({
    TableName: TABLE,
    KeyConditionExpression: "Dept = :dept",
    ExpressionAttributeValues: { ":dept": "HR" },
    ScanIndexForward: true, // ASC(오름차순)
  })
);

console.log("\n📑 Query: Dept='HR'  Age 오름차순");
queryResult.Items?.forEach((item, idx) => {
  console.log(`${idx}. ${item.Name}  -  Age: ${item.Age}`);
});

const items_hr = queryResult.Items ?? []; // 정렬된 리스트
if (items_hr.length >= 3) {
  const third_person = items_hr[2]; // 0,1,2 → 세 번째
  console.log(`\n🔎 HR 부서 세 번째 사람: ${third_person.Name}  (Age: ${third_person.Age})`);
} else {
  console.log("\n⚠️ HR 부서에 세 명 미만의 레코드만 존재합니다.");
}
