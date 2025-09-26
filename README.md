# Todo App with FastAPI, Next.js, and MongoDB

This repository is for an ASU AZNext Vibe Coding project. The application is a todo manager with user authentication, tasks, and labels. The stack is FastAPI for the API, Next.js for the web client, and MongoDB for persistence. The project is delivered in phases and uses a strict set of guardrails for scope and quality.

* No emojis anywhere
* No hyphens in filenames or route segments
* Use plain ASCII punctuation
* Lists use asterisks or numbers

## Quick links to project documentation

* [Project Charter](docs/charter.md)
* [Architecture Overview](docs/architecture.md)
* [Data Model](docs/data_model.md)
* [Phase Plan](docs/phases.md)
* [Git Workflow](docs/git_workflow.md)
* [Swagger Documentation Plan](docs/swagger_plan.md)
* [Quality Gates](docs/quality_gates.md)
* [Guardrails](docs/GUARDRAILS.md)
* [Contributing Guide](CONTRIBUTING.md)
* [Pull Request Checklist](.github/pull_request_template.md)

These files are part of the repository. The agent prompts and plan index are kept outside the repo as requested.

## What is included in the scaffold

This repository ships with a minimal scaffold so that work can proceed in small, graded steps. The scaffold is intentionally light and does not implement business features yet.

### Backend

* FastAPI app with title and version. Swagger at `/docs` and ReDoc at `/redoc`.
* Health endpoint at `/healthz` returns status ok.
* Settings module reads environment values with defaults.
* OpenAPI tags are present as placeholders for auth, users, tasks, and labels.
* No database repositories yet.
* No authentication routes yet.
* No task or label routes yet.

Key files

```
backend/
  app/
    core/
      settings.py
    main.py
```

### Frontend

* Next.js App Router with a simple home page.
* TypeScript configuration ready for development.
* No API calls yet.
* No authentication or tasks user interface yet.

Key files

```
frontend/
  app/
    layout.tsx
    page.tsx
  next.config.ts
  tsconfig.json
  package.json
```

### Governance and quality

* See [Guardrails](docs/GUARDRAILS.md) for the authoritative rules.
* See [Contributing Guide](CONTRIBUTING.md) for flow and local setup.
* Pull request checklist: [.github/pull_request_template.md](.github/pull_request_template.md).
* Pre commit configuration and a guardrails script can be added to enforce rules locally and in continuous integration.

## Phase plan summary

The plan is split into clear phases. See the full text in [Phase Plan](docs/phases.md). This section is an at a glance view.

**Phase zero accounts and setup**  
* Public repository on day one with branch protection
* MongoDB Atlas cluster and user plus secrets saved
* Continuous integration skeleton is created

**Phase one backend core**  
* Authentication with signup, login, logout, and JWT cookie
* Users, tasks, and labels entities with per user scope
* Tasks include title, description, priority, deadline, and status
* Swagger with tags, examples, and a clear error model
* Unit tests for happy paths and authorization guards

**Phase two frontend core**  
* Pages for signup, login, tasks, labels, and profile stub
* Forms with client validation and cookie session
* Task list and create, update, delete
* Assign labels to tasks

**Phase three end to end**  
* Playwright smoke for signup, login, create label, create task with label, toggle status, and delete

**Phase four polish and stretch**  
* Filter by label and profile edit and responsive layout and friendly errors
* README and demo notes updated

## Remaining work in the scaffold

This section lists what the scaffold does not implement yet and the expected place to add each concern.

Backend tasks to complete

* Add MongoDB client helpers under `backend/app/db`
* Add user repository and task and label repositories under `backend/app/db`
* Implement auth routes in `backend/app/api/auth.py` with password hashing and JWT issued as an http only cookie
* Implement tasks routes in `backend/app/api/tasks.py` for list, create, update, and delete with per user scope and indexes for user id and deadline
* Implement labels routes in `backend/app/api/labels.py` for list, create, update, and delete and validate that label ids belong to the current user
* Add structured logging and a shared error response envelope
* Add unit tests for the above

Frontend tasks to complete

* Create pages under `frontend/app` for signup, login, tasks, labels, and profile stub
* Add a small API client under `frontend/lib` to call the backend using `NEXT_PUBLIC_API_BASE_URL`
* Implement basic forms and list pages and assignment of labels during task create or update
* Add a small number of unit tests for forms and utilities

Quality tasks to complete

* Add pre commit configuration and enable it locally
* Add continuous integration for backend and frontend so that lint, type, and tests run on every pull request

## Setup for local development

### Environment variables

Create a file named `.env` under the `backend` with values like these:

```
MONGODB_URI="mongodb+srv://user:password@cluster/dbname?"
JWT_SECRET="change-me"
PROJECT_NAME="Todo App"
```
Create a file named `.env.local` under `frontend` with values like these:

```
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
```

### Starting the services

Backend

```
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Frontend

```
pnpm -C frontend install
pnpm -C frontend dev
```

Swagger UI: http://127.0.0.1:8000/docs

Web app: http://127.0.0.1:3000

## Commit policy and pull requests

* Conventional Commits are required
* Commits should be atomic and readable
* Use feature branches and do not squash merges
* Fill out the pull request checklist and keep continuous integration green

## Change log

A simple change log can be maintained in `CHANGELOG.md`. Add a tag at the end of each phase such as `v0.1.0` for backend core and `v0.2.0` for frontend core.

## Maintainers note

This README will evolve as the project grows. When a phase is delivered, update the sections above and link to the pull requests that completed the work.
