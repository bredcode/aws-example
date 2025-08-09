import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand, ScanCommand, QueryCommand } from "@aws-sdk/lib-dynamodb";
import { v4 as uuidv4 } from "uuid";

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

// 2. Table 객체는 이름만 알면 되므로 별도 생성 코드 불필요

// 첫 번째 아이템  (PK = Dept='HR' ,  SK = Age)
let dept = "HR"; // 파티션 키
let age = Math.floor(Math.random() * 100); // 정렬 키 (0~99)
let emp = uuidv4(); // 부가 정보: EmployeeId

await docClient.send(
  new PutCommand({
    TableName: TABLE,
    Item: {
      Dept: dept,
      Age: age,
      EmpId: emp,
      Name: "Alice",
    },
  })
);
console.log("🆕 CREATE →", dept, age);

// 두 번째 아이템  (Dept='HR', Age = 0~99)
dept = "HR";
age = Math.floor(Math.random() * 100);
emp = uuidv4();

await docClient.send(
  new PutCommand({
    TableName: TABLE,
    Item: {
      Dept: dept,
      Age: age,
      EmpId: emp,
      Name: "Dave",
    },
  })
);
console.log("🆕 CREATE →", dept, age);

// FULL SCAN
const scanRes = await docClient.send(new ScanCommand({ TableName: TABLE }));
const items = scanRes.Items ?? [];

console.log(`📦 전체 데이터 (${items.length}건):`);
items.forEach((item, i) => {
  console.log(`${i + 1}.`, item);
});

// Dept='HR' 기준 Age 오름차순 Query
const queryRes = await docClient.send(
  new QueryCommand({
    TableName: TABLE,
    KeyConditionExpression: "Dept = :dept",
    ExpressionAttributeValues: { ":dept": "HR" },
    ScanIndexForward: true, // ASC(오름차순)
  })
);

console.log("\n📑 Query: Dept='HR'  Age 오름차순");
queryRes.Items?.forEach((item, idx) => {
  console.log(`${idx}. ${item.Name}  -  Age: ${item.Age}`);
});
