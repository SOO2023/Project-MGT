from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
import re


def get_item_by_id(id: int, db: Session, Model, item_name: str = "item"):
    item = db.query(Model).filter(Model.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"{item_name.capitalize()} with id {id} cannot be found."
            },
        )
    return item


def get_all_items(db: Session, Model):
    items = db.query(Model).all()
    return items


def create_new_item(item_dict: dict, db: Session, Model):
    try:
        item = Model(**item_dict)
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error).split(
                "\n")[0].split(")")[-1].strip()},
        )
    else:
        return item


def delete_item(id: int, db: Session, Model, item_name: str = "item"):
    get_item_by_id(id, db, Model, item_name)
    item = db.query(Model).filter(Model.id == id).first()
    db.delete(item)
    db.commit()


def update_item(
    id: int, update_dict: dict, db: Session, Model, item_name: str = "item"
):
    get_item_by_id(id, db, Model, item_name)
    item = db.query(Model).filter(Model.id == id)
    try:
        item.update(update_dict)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        )
    else:
        return item.first()


def str_to_datetime(date_str) -> datetime:
    format = "%d-%m-%Y"
    date = datetime.strptime(date_str, format)
    return date.date()


def is_user_allowed(user_role, endpoint_allowed_role: str = "admin") -> None:
    if user_role != endpoint_allowed_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You have no access to this endpoint."},
        )


def verify_start_end_date(item, start: date, end: date):
    proj_startdate = item.date_created
    proj_deadline = item.deadline
    if proj_startdate > start:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": f"The task start date should not be earlier than the project start date ({proj_startdate})"
            },
        )
    if proj_deadline < end:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": f"The task end date should not be later than the project deadline ({proj_deadline})"
            },
        )


def verify_name(name) -> str | None:
    pattern = r"(^[A-Za-z]+-?[A-Za-z]+$)"
    result = re.findall(pattern=pattern, string=name)
    if not result:
        return None
    return result[0].capitalize()


def home_page() -> str:
    home = """
    <!doctype html>
    <html>
    <head>
    <title>Project Management API</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        h1, h2, h3 {
            color: #333;
        }
        h1 {
            font-size: 2em;
            margin-bottom: 0.5em;
        }
        h2 {
            font-size: 1.75em;
            margin-bottom: 0.5em;
        }
        h3 {
            font-size: 1.5em;
            margin-bottom: 0.5em;
        }
        p {
            margin: 0.5em 0;
        }
        ul {
            margin: 1em 0;
            padding-left: 20px;
        }
        ul li {
            margin-bottom: 0.5em;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: monospace;
        }
    </style>
    </head>
    <body class="bg-light">
    <div class="container bg-white shadow-sm border border-light rounded" style="margin-top: 80px; padding: 10px;">
    <div class="container text-secondary border-bottom" style="text-align:center;">
    <h1>Task 8 FastAPI Backend</h1>
    </div>
    <div class="container" style="margin-top: 30px; padding: 10px;">
    <h4 class="text-body">Project Management API with Multi-Tier Documentation:</h4>
    <p>Develop a fully functional project management API with features like task assignment, deadlines, and progress tracking. Write detailed documentation for different user levels (admin, user, guest) and deploy it using render. </p>
    </div>
    </div>
    <div class="container" style="margin-top: 30px; padding: 10px;">
    <h1>Project Management API Documentation</h1>

    <h2>Overview</h2>
    <p>The Project Management API is designed to facilitate project management through features such as task assignment, deadlines, and progress tracking. It provides role-based access to ensure appropriate permissions and functionalities for different types of users.</p>

    <h2>Features</h2>
    <ul>
        <li><strong>Task Assignment:</strong> Allows for the assignment of tasks to specific users, facilitating accountability and clear responsibilities.</li>
        <li><strong>Deadlines:</strong> Enables setting deadlines for tasks and projects to ensure timely completion.</li>
        <li><strong>Progress Tracking:</strong> Allows tracking the progress of tasks and projects to monitor status and completion rates.</li>
        <li><strong>User Role Management:</strong> Supports different user roles (Admin, User, Guest) with specific permissions and access levels.</li>
    </ul>

    <h2>User Roles and Permissions</h2>

    <h3>Admin</h3>
    <p>Admins have the highest level of access and control within the API. Their responsibilities and capabilities include:</p>
    <ul>
        <li><strong>Project Management:</strong> Create, update, and delete projects.</li>
        <li><strong>Task Management:</strong> Create, update, and delete tasks.</li>
        <li><strong>Progress Tracking:</strong> Update and monitor the progress of projects and tasks.</li>
        <li><strong>User Management:</strong> Manage user accounts, assign roles, and control permissions.</li>
    </ul>

    <h3>User</h3>
    <p>Users have a moderate level of access, mainly focused on their involvement in projects and tasks. Their capabilities include:</p>
    <ul>
        <li><strong>View Projects:</strong> Access and view all projects they are involved in.</li>
        <li><strong>Task Management:</strong> Access and view tasks within projects.</li>
        <li><strong>Progress Tracking:</strong> Update and monitor the progress of tasks and projects they are involved in.</li>
    </ul>

    <h3>Guest</h3>
    <p>Guests have limited, read-only access. Their capabilities include:</p>
    <ul>
        <li><strong>View Projects:</strong> Access and view all projects and specific project details.</li>
        <li><strong>View Tasks:</strong> Access and view tasks within projects.</li>
    </ul>

    <h2>Detailed Workflow</h2>

    <h3>Admin Workflow</h3>
    <ol>
        <li><strong>Register and Login:</strong> Admins register and log in to the API to obtain an authentication token.</li>
        <li><strong>Create Project:</strong> Admins can create new projects, providing necessary details such as project name, description, and deadlines.</li>
        <li><strong>Manage Tasks:</strong> Admins assign tasks to users, setting deadlines and monitoring progress.</li>
        <li><strong>Monitor and Update Progress:</strong> Admins can update the progress of projects and tasks, ensuring timely completion and addressing any issues.</li>
        <li><strong>User Management:</strong> Admins manage user accounts, assigning appropriate roles and ensuring that users have the necessary permissions for their tasks.</li>
    </ol>

    <h3>User Workflow</h3>
    <ol>
        <li><strong>Register and Login:</strong> Users register and log in to the API to obtain an authentication token.</li>
        <li><strong>View Projects:</strong> Users can view the projects they are involved in.</li>
        <li><strong>Manage Tasks:</strong> Users create, update, and delete tasks assigned to them or within their projects, ensuring that they are progressing as planned.</li>
        <li><strong>Update Progress:</strong> Users update the progress of their tasks and projects, providing status updates and marking tasks as complete.</li>
    </ol>

    <h3>Guest Workflow</h3>
    <ol>
        <li><strong>View Projects:</strong> Guests can view all available projects and specific project details, gaining insight into the project's scope and current status.</li>
        <li><strong>View Tasks:</strong> Guests can view tasks within projects, understanding the work being done and its current status.</li>
    </ol>

    <h2>Use Cases</h2>

    <h3>Project Creation and Management (Admin)</h3>
    <ul>
        <li><strong>Creating a New Project:</strong> Admins can create a new project, setting its name, description, and deadlines. This project is then available for task assignments.</li>
        <li><strong>Updating Project Details:</strong> Admins can update project information as needed, including deadlines and descriptions, to reflect changes in scope or priorities.</li>
        <li><strong>Deleting Projects:</strong> Admins can delete projects that are no longer needed or have been completed.</li>
    </ul>

    <h3>Task Management (Admin/User)</h3>
    <ul>
        <li><strong>Assigning Tasks:</strong> Admins or users with appropriate permissions can assign tasks to team members, specifying deadlines and task descriptions.</li>
        <li><strong>Updating Task Status:</strong> Users can update the status of tasks to reflect their progress, such as marking tasks as in-progress or complete.</li>
        <li><strong>Deleting Tasks:</strong> Admins can delete tasks that are no longer relevant or needed.</li>
    </ul>

    <h3>Progress Tracking (Admin/User)</h3>
    <ul>
        <li><strong>Monitoring Progress:</strong> Both admins and users can monitor the progress of tasks and projects, using progress indicators and status updates.</li>
        <li><strong>Updating Progress:</strong> Users update the progress of their assigned tasks, and admins can update overall project progress to ensure visibility and accountability.</li>
    </ul>

    <h3>Viewing Projects and Tasks (Guest)</h3>
    <ul>
        <li><strong>Accessing Project Information:</strong> Guests can view detailed information about projects, including their scope, deadlines, and progress.</li>
        <li><strong>Viewing Task Details:</strong> Guests can view tasks within projects, understanding the work being done and its current status.</li>
    </ul>

    </div>
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return home
