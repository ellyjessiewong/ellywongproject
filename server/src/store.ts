export interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: string;
}

/**
 * Simple in-memory task store. Kept dependency-free (no native modules) so the
 * environment stays easy to build and run in any Cloud Agent VM.
 */
export class TaskStore {
  private tasks = new Map<string, Task>();

  list(): Task[] {
    return [...this.tasks.values()].sort((a, b) =>
      a.createdAt < b.createdAt ? 1 : -1
    );
  }

  create(title: string): Task {
    const trimmed = title.trim();
    if (!trimmed) {
      throw new Error("Title must not be empty");
    }
    const task: Task = {
      id: globalThis.crypto.randomUUID(),
      title: trimmed,
      completed: false,
      createdAt: new Date().toISOString(),
    };
    this.tasks.set(task.id, task);
    return task;
  }

  toggle(id: string): Task | undefined {
    const task = this.tasks.get(id);
    if (!task) return undefined;
    task.completed = !task.completed;
    return task;
  }

  remove(id: string): boolean {
    return this.tasks.delete(id);
  }
}
