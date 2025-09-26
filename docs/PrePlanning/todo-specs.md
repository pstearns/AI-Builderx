## Project Overview
Students will build a full-stack TODO application with user authentication, tasks, and labels. The backend will be a **RESTful API built with Python's FastAPI**, and the frontend will be a **Next.js application**. The application will use **MongoDB** for data persistence. This project is designed to provide hands-on experience with modern web development tools and best practices.

---

## Required Features (Core User Stories)
These are the essential features that must be completed for a passing grade.

* **User Management**
    * **As a user, I want to sign up for an account**, so I can have my own personal task list.
    * **As a user, I want to log in**, so I can access my tasks and manage my profile.
    * **As a user, I want to securely log out**, so my data is protected from others.
* **Task Management**
    * **As a user, I want to create a new task**, so I can add things I need to do to my list.
    * **As a user, I want to view all my tasks**, so I can see everything I need to get done.
    * **As a user, I want to update a task's details**, so I can change its title, description, or status (e.g., incomplete to complete).
    * **As a user, I want to delete a task**, so I can remove completed or irrelevant items from my list.
    * **Required Task Fields**: Every task must include a **title**, an optional **description**, a **priority** level (e.g., High, Medium, Low), and a **deadline** (date).
* **Labeling System**
    * **As a user, I want to create and manage labels (e.g., 'Work,' 'Personal,' 'Urgent')**, so I can categorize and/or prioritize my tasks.
    * **As a user, I want to assign one or more labels to a task**, so I can easily filter and organize my tasks.
* **Data Persistence**
    * The application must **persist all user, task, and label data in a MongoDB database**.

---

## Stretch Goals as User Stories
These features are not required but will demonstrate advanced understanding and improve the user experience.

* **As a user, I want to filter my tasks by label**, so I can quickly find and organize what I need to work on.
* **As a user, I want to be able to edit my profile details**, so I can keep my information up to date.
* **As a user, I want the application to be responsive and work well on different screen sizes**, so I can access my tasks from any device, including my phone or tablet.
* **As a user, I want to see clear, helpful messages when something goes wrong**, so I know what happened and how to proceed.

---

## Technical Requirements & File Structure
Students must adhere to these technical and structural guidelines.

### Database: MongoDB
The project should leverage a MongoDB database filled with appropriately modeled documents & collections. Please reference this document on the MongoDB guidelines for embeding vs referencing information in a document

![](https://i.imgur.com/OwPPuks.png)

### Backend: FastAPI
The project directory should follow a clean, modular structure. Refer to these resources for examples:
* [Simplified FastAPI structure](https://medium.com/@amirm.lavasani/how-to-structure-your-fastapi-projects-0219a6600a8f)
* [Detailed FastAPI best practices](https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable)

### Frontend: Next.js
The project structure should follow best practices for a Next.js application. Refer to these resources for examples:
* [Simplified Next.js structure](https://dev.to/md-afsar-mahmud/folder-structure-for-a-nextjs-project-22fh)
* [Detailed Next.js best practices](https://dev.to/ethanleetech/8-most-customizable-ui-libraries-for-nextjs-24f)

Students must pick one UI library from [this list](https://dev.to/ethanleetech/8-most-customizable-ui-libraries-for-nextjs-24f) for component styling.

### Git & GitHub
* Students must create a **public GitHub repository** for their project.
* The repository URL should be submitted on **Day 1** to an Excel document that will be created for the cohort.
* Students are expected to make **daily commits** with clear, descriptive commit messages. This will be a key part of the evaluation, as it demonstrates consistent progress and version control proficiency.
* They must also create a **`README.md` file** that includes:
    * A brief description of the project.
    * Instructions on how to set up and run the application.
    * A list of technologies used.
    * A list of completed features (and stretch goals, if any).

---

## Project Expectations & Code Integrity
While you are welcome to "vibe code" and explore your creativity, all students will be held accountable for their work.

* **Code Review**: Each student will undergo a **single mandatory code review** with trainer or TA prior to the project's completion. This will be scheduled via a sign-up sheet and is meant to facilitate a deeper understanding of the codebase.
* **Best Practices**: You are expected to follow best practices for code readability, modularity, and maintainability.
* **Code Accountability**: You must be prepared to answer questions and explain the purpose of **any line of your code**.

---

## Submission & Evaluation
* **Submission**: Students will submit a link to their GitHub repository and their project demo video via the provided Excel document.
    * The project demo video must be uploaded as an **unlisted YouTube video**, with the link shared in the submission spreadsheet. [Step-by-Step Guide to Record & Upload Unlisted Video](https://scribehow.com/viewer/How_to_Upload_a_Video_to_YouTube__do3vpp38Qi-FCvxtKeALww)
* **Evaluation**: The project will be evaluated based on a separate rubric.