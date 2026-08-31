# ellywongproject

A small full-stack task manager used to demonstrate the development environment.

- **client/** — React + Vite + TypeScript single-page app (dev server on port `5173`).
- **server/** — Express + TypeScript REST API for tasks (in-memory store, port `3001`).

The Vite dev server proxies `/api/*` requests to the Express server, so the whole
app runs from a single command.

## Prerequisites

- Node.js `>= 20` (this repo pins Node 22 via `.nvmrc`)
- npm `>= 10` (ships with Node)

## Getting started

```bash
npm install          # installs all workspaces (root, client, server)
npm run dev          # starts the API (3001) and the client (5173) together
```

Then open http://localhost:5173 and add a task.

## Useful commands

| Command             | What it does                                        |
| ------------------- | --------------------------------------------------- |
| `npm run dev`       | Runs the API and client dev servers concurrently    |
| `npm run build`     | Type-checks and builds both workspaces               |
| `npm run start`     | Runs the built API server (`server/dist/index.js`)   |
| `npm run lint`      | Lints both workspaces with ESLint                    |
| `npm run typecheck` | Type-checks both workspaces without emitting         |
| `npm test`          | Runs the server API tests (Node test runner)         |

## API

| Method   | Path              | Description            |
| -------- | ----------------- | ---------------------- |
| `GET`    | `/api/health`     | Health check           |
| `GET`    | `/api/tasks`      | List tasks             |
| `POST`   | `/api/tasks`      | Create a task          |
| `PATCH`  | `/api/tasks/:id`  | Toggle task completion |
| `DELETE` | `/api/tasks/:id`  | Delete a task          |

## Cloud Agent environment

`.cursor/environment.json` configures the Cloud Agent dev environment:

- `install`: `npm install`
- `terminals`: a `dev` terminal running `npm run dev`
- `ports`: `5173` (client) and `3001` (api)
