from fastapi import APIRouter, Depends, status, HTTPException
from ..database import db_session
from sqlalchemy.orm import Session
from ..authenticate import get_current_user
from ..models import TaskProgressInfo, Tasks, Projects
from ..schemas import TaskOut, ProgressIn
from ..util import create_new_item, get_item_by_id, update_item, delete_item

router = APIRouter(prefix="/updates", tags=["Task Progress Update"])


@router.post(
    "/tasks/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint allows the task creator and all assigned users to update and comment on the task progress.",
)
def add_task_progress_update(
    task_id: int,
    update: ProgressIn,
    db: Session = Depends(db_session),
    user: dict = Depends(get_current_user),
):
    task = get_item_by_id(task_id, db, Tasks, "task")
    project = get_item_by_id(task.project_id, db, Projects, "project")
    assigned_users = task.assigned_users
    if not assigned_users:
        if project.admin_id != user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "No users currently assigned to this task. Only the task creator can add progress update to this task."
                },
            )
    assigned_users_id = [user.user_id for user in assigned_users]
    all_authorized_users = assigned_users_id + [project.admin_id]
    if user.get("id") not in all_authorized_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the task creator and assigned users assigned can add progress update to this task."
            },
        )
    progress_dict = update.model_dump()
    progress_dict.update({"user_id": user.get("id"), "task_id": task_id})
    _ = create_new_item(progress_dict, db, TaskProgressInfo)
    task_updated = get_item_by_id(task_id, db, Tasks, "task")
    return task_updated


@router.put(
    "/{progress_id}",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint allows assigned users to edit their previous progress update.",
)
def edit_task_progress_update(
    progress_id: int,
    update: ProgressIn,
    db: Session = Depends(db_session),
    user: dict = Depends(get_current_user),
):
    progress_update = get_item_by_id(
        progress_id, db, TaskProgressInfo, "task_progress_update"
    )
    if progress_update.user_id != user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You cannot edit this task progress update."},
        )
    _ = update_item(progress_id, update.model_dump(), db, TaskProgressInfo)
    task_update = get_item_by_id(progress_update.task_id, db, Tasks, "task")
    return task_update


@router.delete(
    "/{progress_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="This endpoint allows assigned users to delete their previous progress update.",
)
def delete_task_progress_update(
    progress_id: int,
    db: Session = Depends(db_session),
    user: dict = Depends(get_current_user),
):
    progress_update = get_item_by_id(
        progress_id, db, TaskProgressInfo, "task_progress_update"
    )
    if progress_update.user_id != user.get("id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You cannot delete this task progress update."},
        )
    delete_item(progress_id, db, TaskProgressInfo, "task_progress_update")
