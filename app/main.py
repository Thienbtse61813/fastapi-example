from fastapi import FastAPI
from app.routers import company, auth, user, task
app = FastAPI()

app.include_router(company.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)

@app.get("/", tags=["Health Check"])

def read_root():
    return {"message": "App is running"}
