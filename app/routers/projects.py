from fastapi import APIRouter, Depends, status, HTTPException
from ..database import db_session
from sqlalchemy.orm import Session
from ..authenticate import get_current_user
from ..models import Projects
from ..schemas import ProjectOut, ProjectIn, ProjectUpdateIn
from ..util import (
    create_new_item,
    get_all_items,
    get_item_by_id,
    update_item,
    delete_item,
    is_user_allowed,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/",
    response_model=list[ProjectOut],
    description="This endpoint allows all users to view all the projectes in the database after they have been authenticated.",
    dependencies=[Depends(get_current_user)],
)
def get_all_projects(db: Session = Depends(db_session)):
    all_projects = get_all_items(db, Projects)
    return all_projects


@router.get(
    "/{project_id}",
    response_model=ProjectOut,
    description="This endpoint allows all users to view specific project by id after they have been authenticated.",
    dependencies=[Depends(get_current_user)],
)
def get_project_by_id(project_id: int, db: Session = Depends(db_session)):
    project = get_item_by_id(project_id, db, Projects, "project")
    return project


@router.post(
    "/",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint can only be accessed by authenticated admins. This endpoint allows the admin to create a new project.",
)
def create_project(
    project_in: ProjectIn,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    project_dict = project_in.model_dump()
    project_dict.update({"admin_id": user.get("id")})
    project = create_new_item(project_dict, db, Projects)
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint can only be accessed by authenticated admins. This endpoint allows admin to edit project they previously created. It ensures that admin can only edit a project they created.",
)
def update_project(
    project_id: int,
    project_update: ProjectUpdateIn,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    user_id = user.get("id")
    is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    project = get_item_by_id(project_id, db, Projects, "project")
    if user_id != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can edit this project."
            },
        )
    project = update_item(
        project_id, project_update.model_dump(), db, Projects, "project"
    )
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="This endpoint can only be accessed by authenticated admins. This endpoint allows admin to delete project they previously created. It ensures that admin can only delete a project they created.",
)
def delete_project(
    project_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    user_id = user.get("id")
    is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    project = get_item_by_id(project_id, db, Projects, "project")
    if user_id != project.admin_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Only the admin with id {project.admin_id} can edit this project."
            },
        )
    delete_item(project_id, db, Projects, "project")
