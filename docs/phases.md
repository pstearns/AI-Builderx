# Phase Plan

**Phase zero accounts and setup**  
Public repository on day one. Readme skeleton. Branch protection. MongoDB Atlas cluster and user. Secrets added to GitHub. Continuous integration skeleton.

**Phase one backend core**  
Authentication with signup login logout and JWT cookie.  
Entities for users tasks and labels.  
Task fields include title description priority deadline and status.  
Per user scoping.  
Swagger with tags examples and error model.  
Unit tests for happy paths and authorization guards.

**Phase two frontend core**  
Pages for signup login tasks labels and profile stub.  
Forms with client side validation.  
Cookie based session.  
Task list and create update delete.  
Assign labels to tasks.

**Phase three end to end**  
Playwright smoke flow for signup login create label create task with label toggle status and delete.

**Phase four polish and stretch**  
Filter by label. Profile edit. Responsive pass. Friendly error messages. Readme and demo notes.  
