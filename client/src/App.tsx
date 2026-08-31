import { useEffect, useState, type FormEvent } from "react";
import { api, type Task } from "./api";

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .list()
      .then(setTasks)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function addTask(e: FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      const task = await api.create(title);
      setTasks((prev) => [task, ...prev]);
      setTitle("");
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function toggleTask(id: string) {
    const updated = await api.toggle(id);
    setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
  }

  async function removeTask(id: string) {
    await api.remove(id);
    setTasks((prev) => prev.filter((t) => t.id !== id));
  }

  const remaining = tasks.filter((t) => !t.completed).length;

  return (
    <main className="app">
      <section className="card">
        <header className="header">
          <h1>Tasks</h1>
          <p className="subtitle">
            {loading
              ? "Loading…"
              : `${remaining} of ${tasks.length} remaining`}
          </p>
        </header>

        <form className="composer" onSubmit={addTask}>
          <input
            className="input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            aria-label="New task title"
          />
          <button className="btn" type="submit">
            Add
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        <ul className="list">
          {tasks.map((task) => (
            <li key={task.id} className={task.completed ? "item done" : "item"}>
              <label className="item-main">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task.id)}
                />
                <span className="item-title">{task.title}</span>
              </label>
              <button
                className="delete"
                onClick={() => removeTask(task.id)}
                aria-label={`Delete ${task.title}`}
              >
                ×
              </button>
            </li>
          ))}
          {!loading && tasks.length === 0 && (
            <li className="empty">No tasks yet — add your first one above.</li>
          )}
        </ul>
      </section>
      <footer className="footer">ellywongproject · full-stack dev environment</footer>
    </main>
  );
}
