import { test } from "node:test";
import assert from "node:assert/strict";
import type { AddressInfo } from "node:net";
import { createApp } from "./app.js";

async function withServer(
  run: (baseUrl: string) => Promise<void>
): Promise<void> {
  const server = createApp().listen(0);
  await new Promise((resolve) => server.once("listening", resolve));
  const { port } = server.address() as AddressInfo;
  try {
    await run(`http://127.0.0.1:${port}`);
  } finally {
    server.close();
  }
}

test("health endpoint reports ok", async () => {
  await withServer(async (baseUrl) => {
    const res = await fetch(`${baseUrl}/api/health`);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.status, "ok");
  });
});

test("creates, lists, toggles and deletes a task", async () => {
  await withServer(async (baseUrl) => {
    const created = await fetch(`${baseUrl}/api/tasks`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ title: "Write docs" }),
    });
    assert.equal(created.status, 201);
    const task = await created.json();
    assert.equal(task.title, "Write docs");
    assert.equal(task.completed, false);

    const listed = await (await fetch(`${baseUrl}/api/tasks`)).json();
    assert.equal(listed.length, 1);

    const toggled = await (
      await fetch(`${baseUrl}/api/tasks/${task.id}`, { method: "PATCH" })
    ).json();
    assert.equal(toggled.completed, true);

    const del = await fetch(`${baseUrl}/api/tasks/${task.id}`, {
      method: "DELETE",
    });
    assert.equal(del.status, 204);

    const afterDelete = await (await fetch(`${baseUrl}/api/tasks`)).json();
    assert.equal(afterDelete.length, 0);
  });
});

test("rejects empty task titles", async () => {
  await withServer(async (baseUrl) => {
    const res = await fetch(`${baseUrl}/api/tasks`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ title: "   " }),
    });
    assert.equal(res.status, 400);
  });
});
