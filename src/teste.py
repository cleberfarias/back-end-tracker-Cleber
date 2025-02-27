import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_connection():
    # Substitua <username>, <password> e <cluster-url> pelos dados do seu cluster Atlas
    MONGO_DETAILS = "mongodb+srv://cleberfdelgado:kyCtZaryRLj4bU3M@cleber-task.zi7ozqr.mongodb.net/?retryWrites=true&w=majority&appName=cleber-task"
    client = AsyncIOMotorClient(MONGO_DETAILS)
    try:
        # Envia um comando 'ping' para testar a conexão
        await client.admin.command('ping')
        print("Conexão com o MongoDB estabelecida com sucesso!")
    except Exception as e:
        print("Erro ao conectar:", e)
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
