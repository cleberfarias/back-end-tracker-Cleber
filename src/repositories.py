# Importa a classe HTTPException do FastAPI para lidar com exceções HTTP
from fastapi import HTTPException
from typing import List  # Importa o tipo List do módulo typing para tipagem de listas
# Importa a classe ObjectId do módulo bson para trabalhar com IDs do MongoDB
from bson import ObjectId

# Função auxiliar para converter o documento do MongoDB em dicionário


def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),  # Converte o ObjectId para string
        "description": task["description"],  # Pega a descrição da tarefa
        # Pega a duração da tarefa em segundos
        "duration_in_seconds": task["duration_in_seconds"],
    }

# Classe repositório para gerenciar tarefas no MongoDB


class TaskRepository:
    def __init__(self, collection):
        self.collection = collection  # Inicializa a classe com a coleção do MongoDB

    # Método assíncrono para criar uma nova tarefa
    async def create_tasks(self, task_data: dict) -> dict:
        # Insere uma nova tarefa na coleção
        result = await self.collection.insert_one(task_data)
        # Busca a tarefa recém-criada
        new_task = await self.collection.find_one({"_id": result.inserted_id})
        # Converte a tarefa para dicionário e retorna
        return task_helper(new_task)

    # Método assíncrono para obter uma tarefa pelo ID
    async def get_task(self, task_id: str) -> dict:
        # Busca a tarefa pelo ID
        task = await self.collection.find_one({"_id": ObjectId(task_id)})
        if task:
            # Converte a tarefa para dicionário e retorna
            return task_helper(task)
        # Lança exceção se a tarefa não for encontrada
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    # Método assíncrono para atualizar uma tarefa pelo ID
    async def update_task(self, task_id: str, update_data: dict) -> dict:
        if update_data:
            result = await self.collection.update_one(
                {"_id": ObjectId(task_id)}, {"$set": update_data}
            )  # Atualiza a tarefa com os novos dados
            if result.modified_count == 1:
                # Busca a tarefa atualizada
                updated_task = await self.collection.find_one({"_id": ObjectId(task_id)})
                # Converte a tarefa para dicionário e retorna
                return task_helper(updated_task)
        # Busca a tarefa existente
        existing_task = await self.collection.find_one({"_id": ObjectId(task_id)})
        if existing_task:
            # Converte a tarefa para dicionário e retorna
            return task_helper(existing_task)
        # Lança exceção se a tarefa não for encontrada
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    # Método assíncrono para deletar uma tarefa pelo ID
    # Método assíncrono para deletar uma tarefa pelo ID


async def delete_task(self, task_id: str) -> dict:
    try:
        clean_task_id = task_id.replace(
            "{", "").replace("}", "")  # Remove { } se houver

        print(f"🔴 Recebido ID para deletar: {clean_task_id}")  # Debug

        # Deleta pelo ID
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
