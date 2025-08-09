// index.mjs  (ES Module, 로컬 메모리 버전)

// 🗄️ 컨테이너 전역 메모리(DB 대용)
// 구조: { id1: { id:"id1", ... }, id2: { ... } }
const mem = {};

// 공통 응답 헬퍼
const res = (code, body) => ({
  statusCode: code,
  body: JSON.stringify(body),
});

export const handler = async (event) => {
  try {
    const { httpMethod, path, pathParameters, body } = event;

    // 1) CREATE  ─ POST /items   (body: { id, ... })
    if (httpMethod === "POST") {
      if (path === "/items") {
        const item = JSON.parse(body);
        if (!item.id) return res(400, "id field required");
        mem[item.id] = item;
        return res(201, item);
      }
    }

    // 2) READ‑ALL ─ GET /items
    if (httpMethod === "GET") {
      if (path === "/items" && !pathParameters?.id) {
        console.log("LOG===========: ", pathParameters);
        return res(200, Object.values(mem));
      }
      // 3) READ‑ONE ─ GET /items/{id}
      if (path.includes("/items") && pathParameters?.id) {
        console.log("LOG===========: ", pathParameters);
        const item = mem[pathParameters.id];
        return item ? res(200, item) : res(404, "Not found");
      }
    }

    // 4) UPDATE ─ PUT /items/{id} (body: { ...fields })
    if (httpMethod === "PUT") {
      if (path.includes("/items") && pathParameters?.id) {
        if (!mem[pathParameters.id]) return res(404, "Not found");
        const updates = JSON.parse(body);
        mem[pathParameters.id] = { ...mem[pathParameters.id], ...updates };
        return res(204, "");
      }
    }

    // 5) DELETE ─ DELETE /items/{id}
    if (httpMethod === "DELETE") {
      if (path.includes("/items") && pathParameters?.id) {
        if (!mem[pathParameters.id]) return res(404, "Not found");
        delete mem[pathParameters.id];
        return res(204, "");
      }
    }

    // 지원하지 않는 라우트
    return res(400, "Bad request");
  } catch (err) {
    console.error(err);
    return res(500, "Internal error");
  }
};
