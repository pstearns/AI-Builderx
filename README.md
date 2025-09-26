# Todo App with FastAPI, Next dot js, and MongoDB

This repository is for a ASU-AZNext-Vibe-Coding project. The application is a todo manager with user authentication, tasks, and labels. The stack is FastAPI for the api, Next dot js for the web client, and MongoDB for persistence. The project is delivered in phases and uses a strict set of guardrails for scope and quality.

* No emojis anywhere
* No hyphens in filenames or route segments
* Use plain ascii punctuation
* Lists use asterisks or numbers

## Quick links to project documentation

* [docs/charter.md](docs/charter.md)
* [docs/architecture.md](docs/architecture.md)
* [docs/data\_model.md](docs/data_model.md)
* [docs/phases.md](docs/phases.md)
* [docs/git\_workflow.md](docs/git_workflow.md)
* [docs/swagger\_plan.md](docs/swagger_plan.md)
* [docs/quality\_gates.md](docs/quality_gates.md)
* [docs/GUARDRAILS.md](docs/GUARDRAILS.md)
* [CONTRIBUTING.md](CONTRIBUTING.md)
* [.github/pull\_request\_template.md](.github/pull_request_template.md)

These files are part of the repository. The agent prompts and plan index are kept outside the repo as requested.

## What is included in the scaffold

This repository ships with a minimal scaffold so that work can proceed in small, graded steps. The scaffold is intentionally light and does not implement business features yet.

### Backend

* FastAPI app with title and version and swagger at slash docs and redoc at slash redoc
* Health endpoint at slash healthz returns status ok
* Settings module reads environment values with defaults
* Openapi tags are present as placeholders for auth, users, tasks, and labels
* No database repositories yet
* No authentication routes yet
* No task or label routes yet

Key files

```
backend/
  app/
    core/
      settings.py
    main.py
```

### Frontend

* Next dot js app router with a simple home page
* Typescript configuration ready for development
* No api calls yet
* No authentication or tasks user interface yet

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

* docs slash GUARDRAILS dot md is the source of truth for rules
* CONTRIBUTING dot md explains flow and local setup
* Pull request checklist is at dot github slash pull underscore request underscore template dot md
* Pre commit configuration and a small guardrails script can be added to enforce the rules locally and in continuous integration

## Phase plan summary

The plan is split into clear phases. The full text is in docs slash phases dot md. This section is an at a glance view.

**Phase zero accounts and setup**  
* Public repository on day one with branch protection
* MongoDB Atlas cluster and user plus secrets saved
* Continuous integration skeleton is created

**Phase one backend core**  
* Authentication with signup login logout and jwt cookie
* Users tasks and labels entities with per user scope
* Tasks include title description priority deadline and status
* Swagger with tags examples and a clear error model
* Unit tests for happy paths and authorization guards

**Phase two frontend core**  
* Pages for signup login tasks labels and profile stub
* Forms with client validation and cookie session
* Task list and create update delete
* Assign labels to tasks

**Phase three end to end**  
* Playwright smoke for signup login create label create task with label toggle status and delete

**Phase four polish and stretch**  
* Filter by label and profile edit and responsive layout and friendly errors
* Readme and demo notes updated

## Remaining work in the scaffold

This section lists what the scaffold does not implement yet and the expected place to add each concern.

Backend tasks to complete

* Add MongoDB client helpers under backend slash app slash db
* Add user repository and task and label repositories under backend slash app slash db
* Implement auth routes in backend slash app slash api slash auth dot py with password hashing and jwt issued as a http only cookie
* Implement tasks routes in backend slash app slash api slash tasks dot py for list create update and delete with per user scope and indexes for user id and deadline
* Implement labels routes in backend slash app slash api slash labels dot py for list create update and delete and validate that label ids belong to the current user
* Add structured logging and a shared error response envelope
* Add unit tests for the above

Frontend tasks to complete

* Create pages under frontend slash app for signup and login and tasks and labels and profile stub
* Add a small api client under frontend slash lib to call the backend using NEXT underscore PUBLIC underscore API underscore BASE underscore URL
* Implement basic forms and list pages and assignment of labels during task create or update
* Add a small number of unit tests for forms and utilities

Quality tasks to complete

* Add pre commit configuration and enable it locally
* Add continuous integration for backend and frontend so that lint type and tests run on every pull request

## Setup for local development

### Environment variables

Create a file named dot env at repository root or under backend with values like these

```
MONGODB_URI="mongodb+srv://..."
JWT_SECRET="change-me"
PROJECT_NAME="Todo App"
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

Swagger is at http colon slash slash one two seven dot zero dot zero dot one colon eight zero zero zero slash docs

The web app is at http colon slash slash one two seven dot zero dot zero dot one colon three zero zero zero

## Commit policy and pull requests

* Conventional Commits are required
* Commits should be atomic and readable
* Use feature branches and do not squash merges
* Fill out the pull request checklist and keep continuous integration green

## Change log

A simple change log can be maintained in CHANGELOG dot md. Add a tag at the end of each phase such as v zero dot one dot zero for backend core and v zero dot two dot zero for frontend core.

## Maintainers note

This readme will evolve as the project grows. When a phase is delivered update the sections above and link to the pull requests that completed the work.
