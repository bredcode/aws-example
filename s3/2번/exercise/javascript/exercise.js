import { S3Client, PutObjectCommand, ListObjectsV2Command, GetObjectCommand } from "@aws-sdk/client-s3";
import fs from "fs";
import path from "path";

// LocalStack에서 사용하는 endpoint 및 region
const LOCALSTACK_ENDPOINT = "https://a45f-61-43-16-236.ngrok-free.app";
const AWS_REGION = "us-east-1";

// boto3 클라이언트 생성
const s3 = new S3Client({
  endpoint: LOCALSTACK_ENDPOINT,
  region: AWS_REGION,
  credentials: {
    accessKeyId: "test", // LocalStack에서는 아무 값이나 사용 가능
    secretAccessKey: "test",
  },
  forcePathStyle: true, // LocalStack 호환을 위해 path-style 필수
});

// 버킷 및 관련 내용 정의
const bucket_name = "my-bucket"; // 이미 만들어 둔 버킷
const local_upload = path.resolve("../dog.jpg"); // 업로드할 원본 이미지
const s3_key = "images/dog.jpg"; // S3 안에서의 경로(Key)
const local_target = path.resolve("downloaded_dog.jpg"); // 내려받을 파일 이름

// 이미지 업로드
// 작은 파일은 put_object, 큰 파일은 upload_file 를 주로 사용
await s3.send(
  new PutObjectCommand({
    Bucket: bucket_name,
    Key: s3_key,
    Body: fs.createReadStream(local_upload),
  })
);
console.log(`✅ 업로드 완료: ${local_upload}  ➜  s3://${bucket_name}/${s3_key}`);

// 버킷 안의 객체 확인
const objects = await s3.send(
  new ListObjectsV2Command({
    Bucket: bucket_name,
    Prefix: "images/",
  })
);
console.log("📂 S3 images/ 폴더 내용:");
for (const obj of objects.Contents || []) {
  console.log("  -", obj.Key);
}

// 이미지 다운로드 (파일 저장)
const { Body } = await s3.send(
  new GetObjectCommand({
    Bucket: bucket_name,
    Key: s3_key,
  })
);
const writeStream = fs.createWriteStream(local_target);
await new Promise((resolve, reject) => {
  Body.pipe(writeStream);
  Body.on("error", reject);
  writeStream.on("finish", resolve);
});
console.log(`📥 다운로드 완료: s3://${bucket_name}/${s3_key}  ➜  ${local_target}`);
