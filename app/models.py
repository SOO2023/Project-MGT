from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from sqlalchemy import ForeignKey
from datetime import datetime, timezone, date


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="in progress")
    startdate: Mapped[date]
    enddate: Mapped[date]
    assigned_users: Mapped[list["AssignUserTask"]] = Relationship(
        backref="task", cascade="all, delete"
    )
    task_progress_detail: Mapped[list["TaskProgressInfo"]] = Relationship(
        backref="task", cascade="all, delete"
    )


class AssignUserTask(Base):
    __tablename__ = "assigntask"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    assigned_tasks: Mapped[list["AssignUserTask"]] = Relationship(
        backref="user", cascade="all, delete"
    )
    created_projects: Mapped[list["Projects"]] = Relationship(
        backref="user", cascade="all, delete"
    )


class TaskProgressInfo(Base):
    __tablename__ = "progress"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_updated: Mapped[date] = mapped_column(
        default=lambda: datetime.now(timezone.utc).date()
    )
    comment: Mapped[str] = mapped_column(nullable=False)
    progress_score: Mapped[int]


class Projects(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    description: Mapped[str]
    date_created: Mapped[date] = mapped_column(
        default=lambda: datetime.now(timezone.utc).date()
    )
    deadline: Mapped[date]
    progress_score: Mapped[int] = mapped_column(default=0)
    status: Mapped[str]
    project_tasks: Mapped[list["Tasks"]] = Relationship(
        backref="project", cascade="all, delete"
    )
