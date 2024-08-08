from fastapi import APIRouter, Depends, status, HTTPException, Body
from ..database import db_session
from sqlalchemy.orm import Session
from ..authenticate import get_current_user
from ..models import Tasks, AssignUserTask, Projects, Users
from ..schemas import TaskOut
from ..util import create_new_item, get_all_items, get_item_by_id, is_user_allowed

router = APIRouter(tags=["Task Assignment"])


@router.post(
    "/tasks/{task_id}/users",
    status_code=status.HTTP_201_CREATED,
    description="This endpoint allow the admin to assign multiple users to a task to a task they created. The endpoint ensure that only users and admins can be assigned to a task. The endpoint will only assign user to a task if at least one of the user is a valid user. It will only return an Exception Error if only all the input ids are invalid or are guests.",
)
def assign_multiple_users_to_a_task(
    task_id: int,
    users_id: list[int] = Body(examples=[[1, 4, 15]]),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    is_user_allowed(user_role=current_user.get("role"), endpoint_allowed_role="admin")
    task = get_item_by_id(task_id, db, Tasks, "task")
    project = get_item_by_id(task.project_id, db, Projects, "project")
    if current_user.get("id") != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can assign users to this task."
            },
        )
    not_found = []
    found = []
    already_added = []
    guest = []
    for user_id in users_id:
        try:
            user = get_item_by_id(user_id, db, Users, "user")
            if user.role == "guest":
                guest.append(user_id)
            else:
                found.append(user_id)
        except:
            not_found.append(user_id)
    if found:
        all_assignments = get_all_items(db, AssignUserTask)
        specific_task_assignments = [
            assign for assign in all_assignments if assign.task_id == task_id
        ]
        for user_id in found:
            try:
                for assign in specific_task_assignments:
                    if assign.user_id == user_id:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail={
                                "message": f"The user with id {user_id} has already been assigned to this task."
                            },
                        )
            except:
                already_added.append(user_id)
            else:
                assignment_dict = {"task_id": task_id, "user_id": user_id}
                _ = create_new_item(assignment_dict, db, AssignUserTask)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"The users are either invalid users or guests.",
                "invalid_users_id": not_found,
                "guest": guest,
            },
        )
    return_dict = {
        "message": f"Users with id {found} were successfully added to task {task_id}",
        "input_ids_details": {
            "valid_users_id": found + guest,
            "invalid_users_id": not_found,
            "previously_added_users_id": already_added,
            "guest_id": guest,
        },
    }
    return return_dict


@router.post(
    "/tasks/{task_id}/{user_id}",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint allow the admin to assign a user to a task. This enpoint will return Exception Error if the input id is either invalid or belongs to a guest.",
)
def assign_one_user_to_a_task(
    task_id: int,
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    is_user_allowed(user_role=current_user.get("role"), endpoint_allowed_role="admin")
    task = get_item_by_id(task_id, db, Tasks, "task")
    user = get_item_by_id(user_id, db, Users, "user")
    project = get_item_by_id(task.project_id, db, Projects, "project")
    if current_user.get("id") != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can assign users to this task."
            },
        )
    if user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"The user with id {user_id} is a guest, and cannot be assigned a task."
            },
        )
    all_assignments = get_all_items(db, AssignUserTask)
    specific_task_assignments = [
        assign for assign in all_assignments if assign.task_id == task_id
    ]
    for assign in specific_task_assignments:
        if assign.user_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": f"The user with id {user_id} has already been assigned to this task."
                },
            )
    assignment_dict = {"task_id": task_id, "user_id": user_id}
    _ = create_new_item(assignment_dict, db, AssignUserTask)
    updated_task = get_item_by_id(task_id, db, Tasks, "task")
    return updated_task


@router.delete(
    "/tasks/{task_id}/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="This endpoint allows the admin to remove a user previously assigned to a task.",
)
def remove_user_from_task(
    task_id: int,
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    is_user_allowed(user_role=current_user.get("role"), endpoint_allowed_role="admin")
    task = get_item_by_id(task_id, db, Tasks, "task")
    _ = get_item_by_id(user_id, db, Users, "user")
    project = get_item_by_id(task.project_id, db, Projects, "project")
    if current_user.get("id") != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can remove users from this task."
            },
        )
    assignment = (
        db.query(AssignUserTask)
        .filter(
            (AssignUserTask.task_id == task_id) & (AssignUserTask.user_id == user_id)
        )
        .first()
    )
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"User {user_id} is not assigned to task {task_id}."},
        )
    db.delete(assignment)
    db.commit()
