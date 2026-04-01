const BACKEND_URL = "http://127.0.0.1:8000";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

const server = Bun.serve({
  port: 3000,

  async fetch(req) {
    const url = new URL(req.url);

    // Handle preflight CORS request
    if (req.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: CORS_HEADERS,
      });
    }

    // Proxy semua request /api/* ke backend Python FastAPI
    if (url.pathname.startsWith("/api")) {
      try {
        const backendUrl = BACKEND_URL + url.pathname + url.search;

        const backendRes = await fetch(backendUrl, {
          method: req.method,
          headers: {
            "Content-Type": "application/json",
          },
          body: req.method !== "GET" ? await req.text() : undefined,
        });

        const data = await backendRes.text();

        return new Response(data, {
          status: backendRes.status,
          headers: {
            "Content-Type": "application/json",
            ...CORS_HEADERS,
          },
        });
      } catch (err) {
        return new Response(
          JSON.stringify({
            error:
              "Backend tidak dapat dijangkau. Pastikan main.py sudah berjalan.",
          }),
          {
            status: 502,
            headers: {
              "Content-Type": "application/json",
              ...CORS_HEADERS,
            },
          },
        );
      }
    }

    // Serve index.html untuk semua route lain
    return new Response(Bun.file("index.html"), {
      headers: {
        "Content-Type": "text/html",
        ...CORS_HEADERS,
      },
    });
  },
});

console.log(
  `✅ FuzzyFinance frontend berjalan di http://localhost:${server.port}`,
);
console.log(`🔗 Proxy /api/* → ${BACKEND_URL}`);
