import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

// 스트림을 문자열로 변환하는 유틸 함수
async function readableStreamToString(stream) {
  const chunks = [];
  for await (const chunk of stream) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf-8");
}

// LocalStack S3 클라이언트 설정
const s3 = new S3Client({
  region: "us-east-1",
  endpoint: "http://localhost:4566", // ngrok 쓰는 경우는 여기 URL 변경
  credentials: {
    accessKeyId: "test",
    secretAccessKey: "test",
  },
  forcePathStyle: true,
});

const bucketName = "my-bucket";
const fileKey = "problem.txt";

async function readProblemFile() {
  const response = await s3.send(
    new GetObjectCommand({
      Bucket: bucketName,
      Key: fileKey,
    })
  );

  const content = await readableStreamToString(response.Body);
  console.log(`📄 Content of ${fileKey}:\n${content}`);
}

await readProblemFile();
