
from fastapi import HTTPException
from typing import List  

from bson import ObjectId




def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "descricao": task.get("descricao", task.get("description", "Sem descrição")),
        "duracaoEmSegundos": task.get("duracaoEmSegundos", 0),
    }


class TaskRepository:
    def __init__(self, collection):
        self.collection = collection  

    async def get_all_tasks(self) -> List[dict]:
        tasks = []
        async for task in self.collection.find():
            tasks.append(task_helper(task))
        return tasks

    
    async def create_tasks(self, task_data: dict) -> dict:
        
        result = await self.collection.insert_one(task_data)
        
        new_task = await self.collection.find_one({"_id": result.inserted_id})
        
        return task_helper(new_task)

    
    async def get_task(self, task_id: str) -> dict:
        
        task = await self.collection.find_one({"_id": ObjectId(task_id)})
        if task:
            
            return task_helper(task)
        
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    
    async def update_task(self, task_id: str, update_data: dict) -> dict:
        if update_data:
            result = await self.collection.update_one(
                {"_id": ObjectId(task_id)}, {"$set": update_data}
            )  
            if result.modified_count == 1:
                
                updated_task = await self.collection.find_one({"_id": ObjectId(task_id)})
                
                return task_helper(updated_task)
        
        existing_task = await self.collection.find_one({"_id": ObjectId(task_id)})
        if existing_task:
            
            return task_helper(existing_task)
        
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    async def get_all_tasks(self) -> List[dict]:
        tasks = []
        async for task in self.collection.find():  
            tasks.append(task_helper(task))  
        return tasks


    async def delete_task(self, task_id: str) -> dict:
        try:
            clean_task_id = task_id.strip().replace(
                "{", "").replace("}", "")  
            print(f"🔴 Recebido ID para deletar: {clean_task_id}")  # Debug

        
            if not ObjectId.is_valid(clean_task_id):
                raise HTTPException(status_code=400, detail="ID inválido")

        
            result = await self.collection.delete_one({"_id": ObjectId(clean_task_id)})

            if result.deleted_count == 1:
                print(
                    f"✅ Tarefa {clean_task_id} deletada com sucesso no banco de dados")
                return {"mensagem": "Tarefa deletada com sucesso"}

            print("❌ Tarefa não encontrada para deletar")
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")

        except Exception as e:
            print("❌ Erro ao deletar tarefa:", str(e))
            raise HTTPException(status_code=500, detail="Erro interno no servidor")
