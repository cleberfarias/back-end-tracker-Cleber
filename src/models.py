
from pydantic import BaseModel

from typing import Optional



class TaskModel(BaseModel):
    
    descricao: str
    
    duracaoEmSegundos: int



class TaskUpdateModel(BaseModel):
    
    descricao: Optional[str] = None
    
    duracaoEmSegundos: Optional[int] = None
