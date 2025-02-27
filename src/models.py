# Importa a classe BaseModel do módulo pydantic, que é usada para criar modelos de dados.
from pydantic import BaseModel
# Importa a classe Optional do módulo typing, que permite que um campo seja opcional.
from typing import Optional


# Define uma classe TaskModel que herda de BaseModel.
class TaskModel(BaseModel):
    # Campo obrigatório do tipo string que armazena a descrição da tarefa.
    descricao: str
    # Campo obrigatório do tipo inteiro que armazena a duração da tarefa em segundos.
    duracaoEmSegundos: int


# Define uma classe TaskUpdateModel que herda de BaseModel.
class TaskUpdateModel(BaseModel):
    # Campo opcional do tipo string que armazena a descrição da tarefa. Pode ser None.
    descricao: Optional[str] = None
    # Campo opcional do tipo inteiro que armazena a duração da tarefa em segundos. Pode ser None.
    duracaoEmSegundos: Optional[int] = None
