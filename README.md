# <center> Raijin-Observer


## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Testes](#testes)
- [Deploy](#deploy)
- [Estrutura do Projeto](#estrutura-do-projeto)

## Sobre o Projeto

Esta aplicação FastAPI tem o objetivo de interagir com aplicações de envio de mensagem e enviar as mesmas para um backend processar.

## Funcionalidades

- Enviar dados ao WhatsApp.
- Escutar alterações do WhatsApp.
- Validação de dados usando Pydantic.
- Documentação automática da API com Swagger e Redoc.
- Testes automatizados com Pytest.
- Deploy em contêineres Docker.

## Pré-requisitos

Antes de começar, você precisará ter as seguintes ferramentas instaladas em sua máquina:

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) (opcional para deploy com contêineres)

## Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento local:

1. Clone o repositório:
   ```bash
   git clone https://github.com/renandias26/raijin-observer.git
   cd raijin-observer
    ````

2. Crie e ative um ambiente virtual:
    ````bash
    python3 -m venv venv # No Windows: py -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ````

    Caso o Windows acuse erro de permissão para ativar o ambiente virtual
    execute o seguinte comando no powershell:
    ```bash
    Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser
    ```


3. Instale as dependências:
    > Desenvolvimento
    ````bash
    pip install -r requirements-dev.txt
    `````

    > Produção
    ````bash
    pip install -r requirements.txt
    ````
## Como Executar
Depois de instalar as dependências, você pode executar a aplicação localmente:
1. Execute a aplicação com Uvicorn:
    ````bash
    uvicorn app.main:app --reload
    ````
    No ambiente de desenvolvimento também é possível executar com fastapi-cli
    ````bash
    fastapi dev app/main.py
    ````
2. Acesse a aplicação em seu navegador:
    - Swagger UI: http://127.0.0.1:8000/docs
    - Redoc: http://127.0.0.1:8000/redoc

## Testes
Para rodar os testes automatizados, utilize o Pytest:

1. Execute todos os testes:
    ````bash
    pytest
    ````
2. Para gerar um relatório de cobertura de código:
    ````bash
    pytest --cov=app tests/
    ````

## Deploy

### Deploy com Docker

Você pode usar Docker para executar a aplicação em um contêiner:

1. Construa a imagem Docker:
    ````bash
    docker build -t fastapi-app .
    ````
2. Execute o contêiner:
    ````bash
    docker run -d -p 8000:8000 fastapi-app
    ````
A aplicação estará disponível em http://127.0.0.1:8000.

### Deploy em Produção
Para deploy em produção, você pode configurar servidores como AWS, Heroku, ou DigitalOcean. Certifique-se de configurar o ambiente de produção adequadamente, incluindo o uso de SSL, balanceamento de carga, e segurança.

## Estrutura do Projeto
````bash
├── app
│   ├── __init__.py
│   ├── main.py          # Ponto de entrada da aplicação
│   ├── models.py        # Definição dos modelos do banco de dados
│   ├── schemas.py       # Definição dos esquemas de Pydantic
│   ├── crud.py          # Operações CRUD
│   ├── dependencies.py  # Dependências de injeção
│   ├── routers
│   │   ├── __init__.py
│   │   ├── items.py     # Rotas para a entidade Item
│   │   └── users.py     # Rotas para a entidade User
│   ├── tests            # Diretório para testes
│   │   ├── __init__.py
│   │   ├── test_main.py # Testes da aplicação
├── .gitignore           # Arquivos e pastas ignorados pelo Git
├── requirements.txt     # Dependências do projeto
├── Dockerfile           # Dockerfile para criação da imagem Docker
├── README.md            # Documentação do projeto

````