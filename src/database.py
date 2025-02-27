from motor.motor_asyncio import AsyncIOMotorClient
# Importa a classe AsyncIOMotorClient do módulo motor.motor_asyncio, que é usada para se conectar a um banco de dados MongoDB de forma assíncrona.

class Database:
    def __init__(self, uri: str, db_name: str):
        # Método construtor da classe Database. É chamado quando uma nova instância da classe é criada.
        self.client = AsyncIOMotorClient(uri)
        # Cria um cliente MongoDB assíncrono usando a URI fornecida.
        self.db = self.client[db_name]
        # Acessa o banco de dados específico usando o nome fornecido.

    def get_collection(self, name: str):
        # Método para obter uma coleção específica do banco de dados.
        return self.db[name]
        # Retorna a coleção com o nome fornecido.