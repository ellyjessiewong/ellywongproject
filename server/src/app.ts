import express, { type Express } from "express";
import cors from "cors";
import { TaskStore } from "./store.js";

export function createApp(store: TaskStore = new TaskStore()): Express {
  const app = express();
  app.use(cors());
  app.use(express.json());

  app.get("/api/health", (_req, res) => {
    res.json({ status: "ok", time: new Date().toISOString() });
  });

  app.get("/api/tasks", (_req, res) => {
    res.json(store.list());
  });

  app.post("/api/tasks", (req, res) => {
    const title = typeof req.body?.title === "string" ? req.body.title : "";
    try {
      const task = store.create(title);
      res.status(201).json(task);
    } catch (err) {
      res.status(400).json({ error: (err as Error).message });
    }
  });

  app.patch("/api/tasks/:id", (req, res) => {
    const task = store.toggle(req.params.id);
    if (!task) {
      res.status(404).json({ error: "Task not found" });
      return;
    }
    res.json(task);
  });

  app.delete("/api/tasks/:id", (req, res) => {
    const removed = store.remove(req.params.id);
    if (!removed) {
      res.status(404).json({ error: "Task not found" });
      return;
    }
    res.status(204).end();
  });

  return app;
}
