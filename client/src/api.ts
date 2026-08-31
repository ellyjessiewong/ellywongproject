export interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: string;
}

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error ?? `Request failed (${res.status})`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  list: () => fetch("/api/tasks").then((r) => json<Task[]>(r)),
  create: (title: string) =>
    fetch("/api/tasks", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ title }),
    }).then((r) => json<Task>(r)),
  toggle: (id: string) =>
    fetch(`/api/tasks/${id}`, { method: "PATCH" }).then((r) => json<Task>(r)),
  remove: async (id: string) => {
    const res = await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`Delete failed (${res.status})`);
  },
};
