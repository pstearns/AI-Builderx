# Quality Gates

**Backend**  
ruff, black check, mypy strict, pytest unit tests. OpenAPI generation must succeed.

**Frontend**  
ESLint, Prettier check, TypeScript no emit. Add unit tests as they are introduced.

**End to end**  
Playwright smoke suite begins in the end to end phase and must pass locally and in continuous integration.

**No printing and no console logging**  
Do not leave print in backend or console dot log in frontend except in tests.
