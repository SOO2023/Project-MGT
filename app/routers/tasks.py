from fastapi import APIRouter, Depends, status, HTTPException
from database import db_session
from sqlalchemy.orm import Session
import util, models, schemas
from authenticate import get_current_user


router = APIRouter(tags=["Tasks"])


@router.post(
    "/projects/{project_id}/tasks",
    response_model=schemas.TaskOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint can only be accessed by the admins. This endpoint ensures that admin can only add tasks to project they have created. Both the start and end dates are validated. The start date cannot be later than the end date, and it cannot be earlier than the date the project was created. Also, the end date cannot be earlier than the start date and it cannot be later than the project deadline date.",
)
def add_task_to_project(
    project_id: int,
    task: schemas.TaskIn,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    util.is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    project = util.get_item_by_id(project_id, db, models.Projects, "project")
    util.verify_start_end_date(project, task.startdate, task.enddate)
    if user.get("id") != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can add tasks to this project."
            },
        )
    task_dict = task.model_dump()
    task_dict.update({"project_id": project_id})
    task = util.create_new_item(task_dict, db, models.Tasks)
    return task


@router.get(
    "/tasks",
    response_model=list[schemas.TaskOut],
    dependencies=[Depends(get_current_user)],
    description="This endpoint ensures users are authenticated before they can view all created tasks.",
)
def get_all_tasks(db: Session = Depends(db_session)):
    all_tasks = util.get_all_items(db, models.Tasks)
    return all_tasks


@router.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskOut,
    dependencies=[Depends(get_current_user)],
    description="This endpoint ensures users are authenticated before they can view a specific tasks.",
)
def get_task_by_id(task_id: int, db: Session = Depends(db_session)):
    task = util.get_item_by_id(task_id, db, models.Tasks, "task")
    return task


@router.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint ensures that admins are authenticated before they can make changes to the tasks they created.",
)
def update_task(
    task_id: int,
    task_in: schemas.TaskIn,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    util.is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    task = util.get_item_by_id(task_id, db, models.Tasks, "task")
    project_id = task.project_id
    project = util.get_item_by_id(project_id, db, models.Projects, "project")
    util.verify_start_end_date(project, task_in.startdate, task_in.enddate)
    if user.get("id") != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can update this task."
            },
        )
    updated_task = util.update_item(
        task_id, task_in.model_dump(), db, models.Tasks, "task"
    )
    return updated_task


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="This endpoint ensures that admins are authenticated before they can delete the tasks they created.",
)
def delete_task(
    task_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    util.is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    task = util.get_item_by_id(task_id, db, models.Tasks, "task")
    project_id = task.project_id
    project = util.get_item_by_id(project_id, db, models.Projects, "project")
    if user.get("id") != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can delete this task."
            },
        )
    util.delete_item(task_id, db, models.Tasks, "task")
