from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator,
    BeforeValidator,
    field_validator,
)
from util import str_to_datetime, verify_name
from typing import Annotated, Literal
from datetime import datetime, timezone, date


class UserAssignInfo(BaseModel):
    project_id: int
    name: str
    startdate: date
    enddate: date


class TaskAssignInfo(BaseModel):
    email: str
    role: str


class UserTask(BaseModel):
    task_id: int
    task: UserAssignInfo


class TaskUser(BaseModel):
    user_id: int
    user: TaskAssignInfo


class Progress(BaseModel):
    comment: str = Field(
        examples=[
            "We have completed the home page frontend design. We are currently working on the about page."
        ]
    )
    progress_score: int = Field(examples=[40])


class ProgressIn(Progress):
    pass


class ProgressOut(Progress):
    task_id: int
    id: int
    user_id: int
    date_updated: date

    class ConfigDict:
        from_attributes = True


class Task(BaseModel):
    name: str = Field(examples=["Frontend Dev"])
    status: Literal["in progress", "completed", "suspended", "cancelled"] = Field(
        examples=["in progress"]
    )
    description: str = Field(examples=["the task is about..."])


class TaskIn(Task):
    startdate: Annotated[date, BeforeValidator(str_to_datetime)] = Field(
        examples=["10-12-2024"]
    )
    enddate: Annotated[date, BeforeValidator(str_to_datetime)] = Field(
        examples=["10-02-2025"]
    )

    @model_validator(mode="after")
    def validate_date_str(cls, values):
        startdate = values.startdate
        enddate = values.enddate
        todaydate = datetime.now(timezone.utc).date()
        if startdate < todaydate:
            raise ValueError(f"The start date should be {todaydate} or later dates.")
        if enddate <= startdate:
            raise ValueError("End date must be a later date to start date.")
        return values


class TaskOut(Task):
    id: int
    project_id: int
    startdate: date
    enddate: date
    assigned_users: list[TaskUser]
    task_progress_detail: list[ProgressOut]

    class ConfigDict:
        from_attributes = True


class Project(BaseModel):
    name: str = Field(examples=["Website frontend and backend development"])
    description: str = Field(examples=["This project is about..."])
    status: Literal["in progress", "completed", "suspended", "cancelled"] = Field(
        examples=["in progress"]
    )


class ProjectIn(Project):
    deadline: Annotated[date, BeforeValidator(str_to_datetime)] = Field(
        examples=["10-12-2024"]
    )

    @model_validator(mode="after")
    def validate_date_str(cls, values):
        date = values.deadline
        todaydate = datetime.now(timezone.utc).date()
        if date < todaydate:
            raise ValueError(f"The deadline should be {todaydate} or later dates.")
        return values


class ProjectUpdateIn(Project):
    progress_score: int


class ProjectOut(Project):
    id: int
    admin_id: int
    deadline: date
    date_created: date
    progress_score: int
    project_tasks: list[TaskOut]

    class ConfigDict:
        from_attributes = True


class ProjectUserOut(BaseModel):
    id: int
    name: str
    status: str
    date_created: date


class User(BaseModel):
    firstname: str = Field(examples=["John"])
    lastname: str = Field(examples=["Doe"])
    email: EmailStr = Field(examples=["jdoe@email.com"])
    role: Literal["admin", "user", "guest"] = Field(examples=["admin"])


class UserIn(User):
    password: str = Field(examples=["secret"], min_length=4)

    @field_validator("firstname")
    @classmethod
    def verify_firstname(cls, v: str):
        result = verify_name(v)
        if not result:
            raise ValueError("The firstname input might some invalid characters.")
        return result

    @field_validator("lastname")
    @classmethod
    def verify_lastname(cls, v: str):
        result = verify_name(v)
        if not result:
            raise ValueError("The lastname input might some invalid characters.")
        return result


class UserOut(User):
    id: int
    created_projects: list[ProjectUserOut]
    assigned_tasks: list[UserTask]
