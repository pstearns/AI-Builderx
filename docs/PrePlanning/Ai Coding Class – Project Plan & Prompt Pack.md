# AI Coding Class – Project Plan & Prompt Pack (v2)

**Owner:** Peter
**Course:** AI Coding (clean, phased rollout)
**Repo:** Public GitHub (Day 1)
**Stack:** FastAPI (Python) + MongoDB + Next.js (TS)
**Methodology:** Trunk‑based, short‑lived feature branches, Conventional Commits, CI on every PR.

---

## 0) Accounts & Online Resources (Day 1)

* **GitHub**: create public repo; add README skeleton; enable branch protection; add issue/PR templates.
* **MongoDB Atlas**: create project + free cluster; DB user; IP allowlist; copy connection string.
* **Secrets**: set `MONGODB_URI`, `JWT_SECRET`, `NEXT_PUBLIC_API_BASE_URL` in GitHub Actions and `.env` (local only).
* **CI Skeleton**: two workflows (`backend.yml`, `frontend.yml`) with lint + typecheck steps; `e2e.yml` placeholder.
* **Commit early**: initial commit + CI green on Day 1.

---

## 1) Project Charter (one page)

**Problem Statement**
Deliver a production‑style, graded TODO app with auth, tasks, and labels, built in phases with verifiable commits and strong documentation.

**Success Criteria**

* MVP user stories completed (auth, task CRUD with required fields, labels).
* MongoDB persistence and indexes.
* Swagger UI enabled with tagged routes and examples.
* Next.js UI consuming the API.
* Daily commits with readable messages; CI green per phase; release tags.

---

## 2) Architecture Overview

**Backend:** FastAPI (3.11+), Pydantic v2, Motor (async MongoDB driver), JWT auth (httpOnly cookie), structured logging.
**Database:** MongoDB Atlas (free/low tier acceptable), indexes for user‑scoped queries.
**Frontend:** Next.js (App Router, TS), **UI kit**: default **shadcn/ui** (Tailwind + Radix) — may swap to any library from the course’s approved list.
**E2E:** Playwright (TS).
**QA:** Ruff + Black + mypy (backend); ESLint + Prettier + `tsc` (frontend).
**Containers:** Dockerfile per app; `docker compose` for local dev.
**Config:** 12‑factor; `.env` never committed.
**Docs:** Swagger UI `/docs`, ReDoc `/redoc`; custom OpenAPI tags & examples.

**Monorepo layout**

```
repo-root/
  backend/
    app/
      api/                 # routers (auth, users, tasks, labels)
      core/                # settings, logging, security
      db/                  # mongo client, repositories
      models/              # pydantic request/response
      main.py              # FastAPI app, swagger config
    tests/
    Dockerfile
    pyproject.toml
  frontend/
    app/                   # Next.js App Router pages
    components/
    lib/
    tests/
    next.config.ts
    package.json
    Dockerfile
  tests-e2e/
    specs/
    playwright.config.ts
  infra/
    docker-compose.yml
    dev.env.example
  .github/workflows/
    backend.yml
    frontend.yml
    e2e.yml
  .editorconfig
  .gitignore
  README.md
  CHANGELOG.md
```

---

## 3) Phase Plan (with acceptance criteria)

### Phase 0 – Accounts, Repo, Atlas, CI

**Deliverables**

* Public repo (Day 1), README skeleton, commit policy, branch protection.
* Atlas cluster + DB user; `.env` local; GH secrets populated; CI skeleton.
  **Acceptance**: CI green; backend connects to Atlas via `docker compose`.

### Phase 1 – Backend Core (FastAPI + Mongo + Swagger)

**Scope**

* **Auth**: signup/login/logout; JWT in httpOnly cookie; password hashing (argon2/bcrypt).
* **CRUD**: users, tasks, labels (per‑user scoping).
* **Task Fields**: title (req), description?, priority (High/Medium/Low), deadline (date), status.
* **Swagger**: tags for auth/users/tasks/labels; examples; documented 401/403/422 responses.
* **Tests**: pytest unit tests for happy paths + guards.
  **Acceptance**: `/healthz` OK; CRUD works against Atlas; CI green; tag `v0.1.0`.

### Phase 2 – Frontend Core (Next.js)

**Scope**

* Pages: `/signup`, `/login`, `/tasks`, `/labels`, `/profile` (stub).
* UI kit wired; forms with Zod validation; API client; state lifted sensibly.
* Auth flow uses cookie‑based session; task list + create/edit/delete; assign labels.
  **Acceptance**: Build passes; can login and perform task CRUD in UI; CI green; tag `v0.2.0`.

### Phase 3 – E2E (Playwright)

**Scope**

* Spec: signup → login → create label → create task with label → toggle done → delete.
* Artifacts uploaded in CI.
  **Acceptance**: E2E green locally & CI; tag `v0.3.0`.

### Phase 4 – Polish & Stretch

**Scope**

* Label filter, profile edit, responsive pass, friendly error states, README finalization, demo video script.
* Optional perf: indexes; `$lookup` to hydrate labels in list view.
  **Acceptance**: Docs/demo complete; tag `v1.0.0`.

---

## 4) Data Model (Mongo)

**users**: `_id`, `email` (unique), `password_hash`, `name`, timestamps.
**labels**: `_id`, `user_id`, `name`, `color`, timestamps; unique `(user_id, name)`.
**tasks**: `_id`, `user_id`, `title`, `description?`, `priority`, `deadline` (date), `status` (open/done), `label_ids: ObjectId[]`, timestamps.
**Indexes**: `users.email`, `labels.(user_id,name)`, `tasks.user_id`, `tasks.label_ids`, `tasks.deadline`.

> Many‑to‑many via **referencing** (`tasks.label_ids`). For UI hydration or label‑based reports, use `$lookup` and aggregation pipelines; simple filtering by `label_id` remains cheap.

---

## 5) Swagger / OpenAPI Plan

* `app = FastAPI(title=..., version=..., docs_url="/docs", redoc_url="/redoc")`
* `openapi_tags` per router (auth, users, tasks, labels).
* Request/response models with `examples`; error envelope `{error: {code, message}}`.
* Security scheme: HTTP bearer; document 401/403.
* Route & field descriptions kept succinct but clear.

---

## 6) Git Workflow & Commit Policy

**Strategy:** Trunk‑based; feature branches; **no squash** to preserve commit history for grading.
**Branch names:** `feat/backend-auth`, `feat/frontend-tasks-ui`, `test/e2e-smoke`, `chore/ci`.
**Conventional Commits:** `feat: add tasks POST`, `fix: correct CORS`, `chore: init ruff`, `docs: update README setup`.
**Cadence:** 3–5 meaningful commits per work session; at least daily during active phases.
**PR template includes:** context, changes, tests, screenshots, rollback plan.

---

## 7) Rubric Mapping → Build Plan

* **MVP user stories (auth, tasks, labels)** → Phases 1–2.
* **MongoDB persistence** → Phase 0 (Atlas) + 1.
* **Next.js + approved UI kit** → Phase 2.
* **Daily commits + README** → Phase 0 onward.
* **Stretch goals** → Phase 4 (label filter, profile edit, responsive, error UX).

---

## 8) Actionable Checklists

### Phase 0 — Commands & Files

* **Backend venv (optional if using Docker)**

```
python -m venv .venv && source .venv/bin/activate # (Windows: .venv\\Scripts\\activate)
pip install fastapi uvicorn[standard] python-multipart pydantic-settings motor passlib[bcrypt] python-jose[cryptography]
pip install ruff black mypy pytest
```

* **Backend skeleton** (minimal): `app/main.py` with FastAPI app, `/healthz`, Swagger enabled.
* **Frontend**

```
pnpm create next-app frontend --ts --eslint --app --src-dir --tailwind
```

* **Docker compose**: API + Frontend + Mongo (optional local) services.
* **CI**: minimal workflows that lint + typecheck; install caches.

### Phase 1 — Backend specifics

* Routers: `auth.py`, `users.py`, `tasks.py`, `labels.py`.
* Repos: `user_repo.py`, `task_repo.py`, `label_repo.py` using Motor.
* Security: password hashing, JWT, dependency for `current_user`.
* Swagger: tags + examples + error schemas.

---

## 9) Agent Prompt Pack

Copy and paste these into your coding agent. They reference `docs/GUARDRAILS.md` and the PR checklist at `.github/pull_request_template.md`. Do not change filenames or structure without an approved Issue.

```text
PROMPT A. Agent master prompt

You are a coding agent working on a university project. Follow the project guardrails strictly.

Constraints
1. Follow docs slash GUARDRAILS dot md in full. If a requested change violates guardrails, stop and request a Scope Change Issue for approval.
2. No emojis anywhere. Use ASCII punctuation only. Lists in markdown use asterisks or numbers.
3. Filenames and route segments must not contain hyphens. Python uses snake case. React components use PascalCase. Next dot js routes use lowercase words without separators.
4. Keep modules small and readable. Prefer reuse over duplication. Add comments that explain the reason.
5. Swagger must remain enabled at slash docs and slash redoc with tags and examples for all routes you touch.
6. Tests must accompany changes when feasible. No print or console dot log outside tests.
7. Use Conventional Commits. Commits must be atomic and readable. No squash merges.
8. Use the PR checklist in dot github slash pull underscore request underscore template dot md.

Working agreement
1. For each task, first list the files you will create or update and a short reason per file.
2. Generate minimal code to satisfy acceptance criteria without adding new features or dependencies unless approved.
3. Output a proposed commit plan of one to three commits with Conventional Commit subjects.
4. Output a short manual test plan.
```

```text
PROMPT P0.1 Repo initialization and governance

Objective
Initialize the repository from the minimal scaffold and add governance files and placeholders without implementing features.

Deliverables
1. README with project description, run instructions, and phase checklist placeholders.
2. docs slash GUARDRAILS dot md with the rules already defined in the class plan.
3. CONTRIBUTING dot md referencing guardrails, pre commit, CI, PR checklist, and Conventional Commits.
4. dot editorconfig and dot gitignore with the AI scratch area paths.
5. PR template at dot github slash pull underscore request underscore template dot md.
6. commitlint config and workflow. pre commit config and a simple guardrails check script that enforces no emojis and no hyphens in filenames.

Acceptance criteria
1. Repo layout matches the Architecture Overview. No new top level folders.
2. Guardrails document exists and is linked from README and CONTRIBUTING.
3. Pre commit runs locally and the guardrails script passes.

Commit plan
1. docs: add guardrails and contributing
2. chore: add repo meta and PR template
3. ci: add commit lint and pre commit hooks
```

```text
PROMPT P0.2 CI skeleton

Objective
Create minimal GitHub Actions workflows for backend and frontend that lint and type check but do not require full builds.

Deliverables
1. dot github slash workflows slash backend dot yml with python setup and lint type steps.
2. dot github slash workflows slash frontend dot yml with node and lint steps.
3. dot github slash workflows slash commitlint dot yml wired to the commitlint config.

Acceptance criteria
1. Workflows trigger on pull requests and main branch pushes.
2. CI passes with the current minimal scaffold.

Commit plan
1. ci: add backend workflow
2. ci: add frontend workflow
3. ci: add commit message linting
```

```text
PROMPT P0.3 Environment and secrets readiness

Objective
Prepare for MongoDB Atlas and local env without adding business logic.

Deliverables
1. Sample env entries in README for MONGODB underscore URI and JWT underscore SECRET and PROJECT underscore NAME.
2. Update settings module to read env file and expose project name and version.

Acceptance criteria
1. uvicorn backend dot app dot main colon app runs and slash healthz returns status ok.
2. No new dependencies beyond those already allowed.

Commit plan
1. docs: add env examples and local run notes
2. chore: refine settings for env loading
```

```text
PROMPT P1.1 Backend foundations settings and Mongo client

Objective
Add a settings module and a Motor client factory with dependency helpers. Do not add repositories or CRUD yet.

Deliverables
1. backend slash app slash core slash settings dot py with typed settings and env file support.
2. backend slash app slash db slash mongo dot py with AsyncIOMotorClient factory and get underscore db helper.
3. Confirm FastAPI app exposes slash docs and slash redoc and returns openapi.

Acceptance criteria
1. Running uvicorn returns healthy slash healthz.
2. No direct database operations are implemented.

Commit plan
1. feat: add settings and Mongo client factory
2. docs: update README run instructions
```

```text
PROMPT P1.2 Auth skeleton

Objective
Implement signup, login, and logout routes with password hashing and JWT issued as an httpOnly cookie. Keep logic minimal and secure. Do not implement profile edit.

Deliverables
1. backend slash app slash api slash auth dot py with signup login logout endpoints and request models.
2. Password hashing with bcrypt or argon two and JWT using a library such as python jose. Abstract secrets through settings.
3. Swagger tags and examples for each route. Error envelope with code and message.
4. Unit tests for happy path signup and login with TestClient mocking the database where needed.

Acceptance criteria
1. Users can sign up and receive a token. Users can log in and receive a token. Logout clears cookie.
2. All routes are documented in Swagger with examples and 401 403 422 responses.
3. Tests pass locally and in CI.

Commit plan
1. feat: add auth routes with jwt cookie
2. test: add auth happy paths
3. docs: add swagger examples for auth
```

```text
PROMPT P1.3 Tasks minimal CRUD

Objective
Implement per user scoped tasks with required fields title description optional priority deadline status and label underscore ids referencing. Keep persistence simple and avoid premature optimization.

Deliverables
1. backend slash app slash models slash schemas dot py entries for TaskCreate and TaskPublic with examples.
2. backend slash app slash api slash tasks dot py routes for list create update delete using the Mongo client. Add basic indexes for user id and deadline.
3. Swagger tags and examples and documented errors.
4. Unit tests for create list and update.

Acceptance criteria
1. All task routes work against MongoDB when MONGODB underscore URI is configured.
2. Per user scoping enforced via the current user dependency.
3. Swagger and tests are green.

Commit plan
1. feat: add task models and routes
2. test: add task happy paths
3. docs: swagger examples for tasks
```

```text
PROMPT P1.4 Labels minimal CRUD and assignment

Objective
Implement labels per user with unique name per user and allow assigning labels to tasks by id reference. Do not add reports.

Deliverables
1. backend slash app slash models entries for LabelCreate and LabelPublic.
2. backend slash app slash api slash labels dot py routes for list create update delete.
3. Update tasks routes to accept label ids in create and update. Add validation that label ids belong to the current user.
4. Swagger examples and unit tests for label creation and task assignment.

Acceptance criteria
1. Labels are unique by user and name.
2. Task creation or update with label ids succeeds when the labels belong to the user and fails otherwise.
3. CI green.

Commit plan
1. feat: add label models and routes
2. feat: support task label assignment
3. test: label and assignment paths
```

```text
PROMPT P1.5 Error handling and logging

Objective
Introduce structured logging and a consistent error response envelope. Remove print calls.

Deliverables
1. Logging setup in backend slash app slash core. Use standard library logging with json friendly fields where possible.
2. Error handler that returns error envelope with code and message for known cases.
3. Update existing routes to use the error helpers.

Acceptance criteria
1. No print calls remain.
2. Error responses are documented in Swagger.

Commit plan
1. chore: add structured logging and error helpers
2. refactor: adopt error envelope in routes
```

```text
PROMPT P2.1 Frontend foundations and auth forms

Objective
Set up Next dot js pages for signup login tasks and labels and a simple api client. Do not implement complex state. Use the approved UI library if requested otherwise keep plain HTML for now.

Deliverables
1. Pages under frontend slash app slash signup and slash login and slash tasks and slash labels.
2. Simple forms that call the backend auth routes and store session via httpOnly cookie. On success redirect to slash tasks.
3. Api client under frontend slash lib slash api dot ts that reads NEXT underscore PUBLIC underscore API underscore BASE underscore URL.
4. Basic unit test for one form submit if feasible.

Acceptance criteria
1. Manual flow works against the running backend for signup login and a simple task list.
2. No console dot log remains outside tests.

Commit plan
1. feat: add auth forms and api client
2. feat: add tasks and labels pages placeholders
3. test: basic form submit test
```

```text
PROMPT P2.2 Tasks and labels UI

Objective
Implement the minimal UI for listing tasks creating a task and listing labels creating a label and assigning labels when creating or updating a task.

Deliverables
1. Components under frontend slash components that remain small and readable.
2. Client calls to the backend for list and create and update.
3. Error messages for failed requests without leaking details.

Acceptance criteria
1. A user can create a label then create a task with that label then mark complete then delete the task.
2. Pages pass TypeScript and ESLint.

Commit plan
1. feat: tasks list and create
2. feat: labels list and create
3. refactor: extract small components
```

```text
PROMPT P3.1 Playwright end to end

Objective
Add an end to end smoke that covers signup login create label create task with that label toggle status and delete.

Deliverables
1. tests underscore e2e folder with Playwright config and a single spec that runs headless.
2. GitHub Action that runs the spec and uploads artifacts on failure.

Acceptance criteria
1. Spec is deterministic and passes locally and in CI when backend and frontend are running.

Commit plan
1. test: add e2e smoke for core flow
2. ci: add e2e workflow
```

```text
PROMPT P4.1 Polish and stretch

Objective
Add label filter in tasks page and friendly error states and responsive layout and optional profile edit. Do not change the data model without approval.

Deliverables
1. Filter control on tasks page that queries backend by label id.
2. User friendly error components.
3. Minor responsive improvements.
4. Profile edit is optional and must stay simple.

Acceptance criteria
1. Filter works and UI remains readable on small screens.
2. All existing tests pass.

Commit plan
1. feat: label filter on tasks page
2. feat: error states and responsive tweaks
3. docs: update README and demo steps
```
