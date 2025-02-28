from fastapi import FastAPI, HTTPException
from typing import List
from .models import TaskModel, TaskUpdateModel
from .database import Database
from .repositories import TaskRepository
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient



app = FastAPI()  

origins = [
    "https://cleber-tracker.vercel.app",  
    "http://localhost:8080",  
    "http://127.0.0.1:8080" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_DETAILS = "mongodb+srv://cleberfdelgado:kyCtZaryRLj4bU3M@cleber-task.zi7ozqr.mongodb.net/?retryWrites=true&w=majority&appName=cleber-task"

DB_NAME = "cleber-task"


client = AsyncIOMotorClient(MONGO_DETAILS)
db = client[DB_NAME]
task_collection = db["tasks"]


task_repository = TaskRepository(task_collection)

db = Database(MONGO_DETAILS, DB_NAME)
task_collection = db.get_collection("tasks")
task_repository = TaskRepository(task_collection)

@app.get("/")  # ✅ Para testar se a API está rodando
async def root():
    return {"message": "API está rodando!"}

@app.post("/tasks", response_model=dict)
async def create_task(task: TaskModel):
    
    task_data = task.dict()
    return await task_repository.create_tasks(task_data)


@app.get("/tasks", response_model=List[dict])
async def list_tasks():
    return await task_repository.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=dict)
async def get_task(task_id: str):
    return await task_repository.get_task(task_id)


@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: str, task: TaskUpdateModel):
    update_data = {k: v for k, v in task.dict().items() if v is not None}
    return await task_repository.update_task(task_id, update_data)


@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    return await task_repository.delete_task(task_id)
# ✅ Fechando a conexão com o banco ao desligar a API
@app.on_event("shutdown")
async def shutdown_db_client():
    print("🛑 Fechando conexão com MongoDB...")
    client.close()