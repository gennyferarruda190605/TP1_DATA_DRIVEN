from fastapi import APIRouter
from models import Saudacao, Usuario, Dados_Usuario, Dados_Aniversario
from fastapi import HTTPException
from datetime import date

router = APIRouter()

lista_usuarios = [Dados_Usuario(id=0 ,username='Gennyfer', age=2)]


@router.get('/')
async def entrada():
    return {'mensage': 'Hello, FastAPI!'}


@router.get('/status')
async def status_api():
    return {'status': 'API Disponível'}


@router.get('/user_semresponse/{username}') #
async def cumprimento_sem_responde(username: str):
    return {'mensage': f'Olá {username}, seja bem-vindo(a)'}


@router.get('/user/{username}', response_model=Saudacao)
async def cumprimento_com_response(username: str):
    for usuario in lista_usuarios:
        if usuario.username == username:
            return {
                'username': usuario.username,
                'message': f'Olá, {usuario.username}! Seja bem-vindo(a).'
            }
    raise HTTPException(
        status_code=404,
        detail=f'Usuário ({username}) não encontrado! Cadastrar usuário com método POST abaixo')

    
@router.post('/create-user', status_code=201, response_model=Usuario)
async def criacao_usuario(dados : Usuario):
    novo_usuario = Dados_Usuario(
            id=len(lista_usuarios),
            username=dados.username,
            age=dados.age
        )
    lista_usuarios.append(novo_usuario)
    return novo_usuario

@router.get('/users', response_model=list[Usuario]) #
async def usuarios():
    return lista_usuarios


@router.get('/item/{id}', response_model=Usuario)
async def id_usuario(id : int):
    for usuario in lista_usuarios:
        if usuario.id == id:
            return usuario

    raise HTTPException(
        status_code=404,
        detail=f'Usuário com id {id} não foi encontrado.'
        )


@router.delete('/item/{id}')
async def excluir_usuario(id: int):
    for indice, usuario in enumerate(lista_usuarios):
        if usuario.id == id:
            lista_usuarios.pop(indice)
            return {'message': f'Usuário com id {id} removido com sucesso.'}

    raise HTTPException(
        status_code=404,
        detail=f'Usuário com id {id} não foi encontrado.'
        )


@router.post('/birthday')
async def calcular_aniversario(dados: Dados_Aniversario):
    data_atual = date.today()
    prox_aniversario = dados.data_nascimento.replace(year=data_atual.year)

    if prox_aniversario < data_atual:
        prox_aniversario = dados.data_nascimento.replace(year=data_atual.year + 1)

    dias = (prox_aniversario - data_atual).days

    return {
        'name' : dados.name,
        'proximo_aniversario' : prox_aniversario,
        'message': f'Olá, {dados.name}! Faltam {dias} dias para o seu próximo aniversário.'
        }

