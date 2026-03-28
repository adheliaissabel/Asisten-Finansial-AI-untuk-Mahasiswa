const server = Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response(Bun.file("index.html"), {
      headers: { "Content-Type": "text/html" },
    });
  },
});
console.log(`Frontend berjalan di http://localhost:${server.port}`);