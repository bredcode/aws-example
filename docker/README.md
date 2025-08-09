```sh
# 도커 제거
docker rm -f localstack

# 도커 실행 (서비스 포함시켜서)
docker run --name localstack -d -p 4566:4566 -e SERVICES=s3,dynamodb,lambda -e DEBUG=1 localstack/localstack
```

```sh
# 또는 도커 컴포즈 실행 (git bash에서 진행)
docker compose up -d

# docker compose 다시 시작
docker-compose down
```
