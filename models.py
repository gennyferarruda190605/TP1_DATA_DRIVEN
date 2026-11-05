from pydantic import BaseModel
from datetime import date

class Saudacao(BaseModel):
    username : str
    message : str


class Dados_Usuario(BaseModel):
    id: int
    username: str
    age: int

class Usuario(BaseModel):
    username: str
    age: int

class Dados_Aniversario(BaseModel):
    name: str 
    data_nascimento: date


