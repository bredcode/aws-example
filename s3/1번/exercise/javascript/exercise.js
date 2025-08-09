import {
  S3Client,
  DeleteObjectCommand,
  ListBucketsCommand,
  PutObjectCommand,
  ListObjectsV2Command,
  GetObjectCommand,
} from "@aws-sdk/client-s3";

export async function readableStreamToString(stream) {
  const chunks = [];
  for await (const chunk of stream) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf-8");
}

// LocalStack 설정
const s3 = new S3Client({
  region: "us-east-1",
  endpoint: " https://70f9-61-43-16-236.ngrok-free.app",
  credentials: {
    accessKeyId: "test",
    secretAccessKey: "test",
  },
  forcePathStyle: true, // LocalStack에서 필요
});

const bucketName = "my-bucket";
const fileKey = "js_test.txt";
const fileContent = "Hello, LocalStack With JavaScript!";

// 1. 파일 업로드
await s3.send(
  new PutObjectCommand({
    Bucket: bucketName,
    Key: fileKey,
    Body: fileContent,
  })
);
console.log(`📤 Uploaded ${fileKey} to ${bucketName}`);

// 2. 버킷 목록 조회
const buckets = await s3.send(new ListBucketsCommand());
console.log("📂 Buckets:");
buckets.Buckets.forEach((b) => console.log(" -", b.Name));

// 3. 객체 목록 조회
const objects = await s3.send(new ListObjectsV2Command({ Bucket: bucketName }));
console.log(`📂 Files in ${bucketName}:`);
(objects.Contents || []).forEach((obj) => console.log(" -", obj.Key));

// 4. 객체 다운로드 및 출력
const file = await s3.send(new GetObjectCommand({ Bucket: bucketName, Key: fileKey }));
const content = await readableStreamToString(file.Body);
console.log(`📄 Content of ${fileKey}:\n${content}`);

// 5. 객체 삭제
await s3.send(
  new DeleteObjectCommand({
    Bucket: bucketName,
    Key: fileKey,
  })
);
console.log(`🗑️  Deleted object: ${fileKey}`);

// 6. 객체 목록 조회
const remainObjects = await s3.send(new ListObjectsV2Command({ Bucket: bucketName }));
console.log(`📂 Files in ${bucketName}:`);
(remainObjects.Contents || []).forEach((obj) => console.log(" -", obj.Key));
