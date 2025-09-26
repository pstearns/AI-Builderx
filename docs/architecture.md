# Architecture Overview

**Backend**  
FastAPI with Python three eleven or higher, Pydantic version two, Motor client for MongoDB, JWT authentication using http only cookie, structured logging.

**Database**  
MongoDB Atlas free tier is acceptable. Create indexes for user scoped queries.

**Frontend**  
Next dot js with App Router and TypeScript. Choose one approved user interface library or default to shadcn slash ui. The choice must be recorded in the readme.

**End to end and quality**  
Playwright for end to end in a later phase. Ruff, Black, mypy for backend. ESLint, Prettier, and TypeScript for frontend.

**Configuration**  
Twelve factor style environment file. Secrets are not committed.  

**Documentation**  
Swagger user interface at slash docs and ReDoc at slash redoc with tags and examples.
