from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from util import home_page
from routers import auth, projects, users, tasks, assign_task, task_progress
from database import Base, engine


Base.metadata.create_all(engine)

with open("./description.txt", "r") as f:
    description = f.read()

app = FastAPI(
    description=description,
    summary="The Project Management API facilitates efficient project management by allowing task assignment, setting deadlines, and tracking progress. It supports role-based access with specific permissions for Admins, Users, and Guests, ensuring secure and effective collaboration within teams.",
)


@app.get("/", tags=["Home"], description="This is the home page.")
def root():
    return HTMLResponse(home_page())


all_routers = [
    auth.router,
    projects.router,
    users.router,
    tasks.router,
    assign_task.router,
    task_progress.router,
]

for router in all_routers:
    app.include_router(router)
