import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  PutCommand,
  GetCommand,
  UpdateCommand,
  ScanCommand,
  DeleteCommand,
} from "@aws-sdk/lib-dynamodb";
import { v4 as uuidv4 } from "uuid";

const ENDPOINT = "http://localhost:4566";
const REGION = "us-east-1";
const TABLE = "Users";

// 클라이언트 생성
const ddbClient = new DynamoDBClient({
  endpoint: ENDPOINT,
  region: REGION,
  credentials: { accessKeyId: "test", secretAccessKey: "test" },
});
const docClient = DynamoDBDocumentClient.from(ddbClient);

// CREATE
let userId = uuidv4();
await docClient.send(
  new PutCommand({
    TableName: TABLE,
    Item: {
      UserId: userId,
      Name: "Alice",
      Age: 29,
      Item: {
        ProductId: "P‑100",
        Price: 19.99,
      },
    },
  })
);
console.log("🆕 CREATE →", userId);

// READ
let ret = await docClient.send(
  new GetCommand({
    TableName: TABLE,
    Key: { UserId: userId },
  })
);
console.log("📄 READ:", ret.Item);

// CREATE
userId = uuidv4();
await docClient.send(
  new PutCommand({
    TableName: TABLE,
    Item: {
      UserId: userId,
      Name: "Dave",
      Age: 20,
    },
  })
);
console.log("🆕 CREATE →", userId);

// READ
ret = await docClient.send(
  new GetCommand({
    TableName: TABLE,
    Key: { UserId: userId },
  })
);
console.log("📄 READ:", ret.Item);

// UPDATE  (Name → Bob, Age → 30)
await docClient.send(
  new UpdateCommand({
    TableName: TABLE,
    Key: { UserId: userId },
    UpdateExpression: "SET #n = :name, #a = :age",
    ExpressionAttributeNames: {
      "#n": "Name",
      "#a": "Age",
    },
    ExpressionAttributeValues: {
      ":name": "Bob",
      ":age": 30,
    },
  })
);
console.log("✏️  UPDATE");

// FULL SCAN
const scanRes = await docClient.send(new ScanCommand({ TableName: TABLE }));
const items = scanRes.Items ?? [];

console.log(`📦 전체 데이터 (${items.length}건):`);
items.forEach((item, idx) => console.log(`${idx + 1}.`, item));

// DELETE (두 번째 아이템 삭제)
await docClient.send(
  new DeleteCommand({
    TableName: TABLE,
    Key: { UserId: userId },
  })
);
console.log("❌ DELETE");
