from fastapi import APIRouter, Depends, status
from ..database import db_session
from sqlalchemy.orm import Session
from ..authenticate import HashVerifyPassword, get_current_user
from ..schemas import UserIn, UserOut
from ..models import Users
from ..util import (
    create_new_item,
    get_all_items,
    get_item_by_id,
    update_item,
    delete_item,
    is_user_allowed,
)

hash_password = HashVerifyPassword()
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    description="This endpoint allows users to create an account. The endpoint has several validations. Both firstname and lastname are validate not to include irrelevant characters. Email field ensures that the str entered follows email pattern. The password field ensures that password characters is not less than 4. ",
)
def add_user(user: UserIn, db: Session = Depends(db_session)):
    user.password = hash_password.hash_password(user.password)
    user = create_new_item(user.model_dump(), db, Users)
    return user


@router.get(
    "/",
    response_model=list[UserOut],
    description="This endpoint allows admin to query all users in the database. The endpoint can only be accessed by the admins after they have been authenticated successfully.",
)
def get_all_users(
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    users = get_all_items(db, Users)
    return users


@router.get(
    "/profile",
    response_model=UserOut,
    description="This endpoint is used to get current user profile. This endpoint gives the user an overview of their profile, and can only be accessed after being authenticated.",
)
def get_current_user_profile(
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    user = get_item_by_id(user.get("id"), db, Users, "user")
    return user


@router.get(
    "/{user_id}",
    response_model=UserOut,
    description="This endpoint allows the admin to get specific user in the database. This endpoint can only be accessed by the admins after they have been authenticated successfully.",
)
def get_user(
    user_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    user = get_item_by_id(user_id, db, Users, "user")
    return user


@router.put(
    "/",
    response_model=UserOut,
    description="This endpoint is used by users to update their information. Users must be authenticated before their profile can be updated.",
    status_code=status.HTTP_201_CREATED,
)
def update_user_info(
    user_info: UserIn,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    user_id = user.get("id")
    user_info.password = hash_password.hash_password(user_info.password)
    user = update_item(user_id, user_info.model_dump(), db, Users, "user")
    return user


@router.delete(
    "/{user_id}",
    description="This endpoint is used to allow admin delete users. Admins must first be authenticated before they can delete any user.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(db_session),
):
    is_user_allowed(user_role=user.get("role"), endpoint_allowed_role="admin")
    delete_item(user_id, db, Users, "user")
