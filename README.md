# Project Management API Documentation

## Overview

The Project Management API is designed to facilitate project management through features such as task assignment, deadlines, and progress tracking. It provides role-based access to ensure appropriate permissions and functionalities for different types of users.

## Features

1. **Task Assignment**: Allows for the assignment of tasks to specific users, facilitating accountability and clear responsibilities.
2. **Deadlines**: Enables setting deadlines for tasks and projects to ensure timely completion.
3. **Progress Tracking**: Allows tracking the progress of tasks and projects to monitor status and completion rates.
4. **User Role Management**: Supports different user roles (Admin, User, Guest) with specific permissions and access levels.

## User Roles and Permissions

### Admin
Admins have the highest level of access and control within the API. Their responsibilities and capabilities include:

- **Project Management**: Create, update, and delete projects.
- **Task Management**: Create, update, and delete tasks.
- **Progress Tracking**: Update and monitor the progress of projects and tasks.
- **User Management**: Manage user accounts, assign roles, and control permissions.

### User
Users have a moderate level of access, mainly focused on their involvement in projects and tasks. Their capabilities include:

- **View Projects**: Access and view all projects they are involved in.
- **Task Management**: Access and view tasks within projects.
- **Progress Tracking**: Update and monitor the progress of tasks and projects they are involved in.

### Guest
Guests have limited read-only access. Their capabilities include:

- **View Projects**: Access and view all projects and specific project details.
- **View Tasks**: Access and view tasks within projects.

## Detailed Workflow

### Admin Workflow

1. **Register and Login**: Admins register and log in to the API to obtain an authentication token.
2. **Create Project**: Admins can create new projects, providing necessary details such as project name, description, and deadlines.
3. **Manage Tasks**: Admins assign tasks to users, setting deadlines and monitoring progress.
4. **Monitor and Update Progress**: Admins can update the progress of projects and tasks, ensuring timely completion and addressing any issues.
5. **User Management**: Admins manage user accounts, assigning appropriate roles and ensuring that users have the necessary permissions for their tasks.

### User Workflow

1. **Register and Login**: Users register and log in to the API to obtain an authentication token.
2. **View Projects**: Users can view the projects they are involved in.
3. **Manage Tasks**: Users view tasks assigned to them or within their projects, ensuring that they are progressing as planned.
4. **Update Progress**: Users update the progress of their tasks and projects, providing status updates and marking tasks as complete.

### Guest Workflow

1. **View Projects**: Guests can view all available projects and specific project details, gaining insight into the project's scope and current status.
2. **View Tasks**: Guests can view tasks within projects, understanding the work being done and its current status.

## Use Cases

### Project Creation and Management (Admin)
- **Creating a New Project**: Admins can create a new project, setting its name, description, and deadlines. This project is then available for task assignments.
- **Updating Project Details**: Admins can update project information as needed, including deadlines and descriptions, to reflect changes in scope or priorities.
- **Deleting Projects**: Admins can delete projects that are no longer needed or have been completed.

### Task Management (Admin/User)
- **Assigning Tasks**: Admins can assign tasks to team members, specifying deadlines and task descriptions.
- **Updating Task Status**: Users can update the status of tasks to reflect their progress, such as marking tasks as in-progress or complete.
- **Deleting Tasks**: Admins can delete tasks that are no longer relevant or needed.

### Progress Tracking (Admin/User)
- **Monitoring Progress**: Both admins and users can monitor the progress of tasks and projects, using progress indicators and status updates.
- **Updating Progress**: Users update the progress of their assigned tasks, and admins can update overall project progress to ensure visibility and accountability.

### Viewing Projects and Tasks (Guest)
- **Accessing Project Information**: Guests can view detailed information about projects, including their scope, deadlines, and progress.
- **Viewing Task Details**: Guests can view tasks within projects, understanding the work being done and its current status.
