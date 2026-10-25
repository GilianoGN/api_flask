# 🚀 Flask REST API - RBAC, JWT, Automated Testing & Swagger Documentation
Uma API REST profissional, robusta e desenvolvida em Python/Flask, contando com autenticação JWT, controle de acesso baseado em papéis hierárquicos (RBAC), documentação interativa automatizada (Swagger UI / Apispec) e uma suíte completa de testes de integração.

---

## 📌 Sumário
- [Visão Geral](#-visão-geral)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura & Estrutura do Projeto](#-arquitetura--estrutura-do-projeto)
- [Controle de Acesso (RBAC)](#-controle-de-acesso-rbac)
- [Documentação da API (Swagger UI)](#-documentação-da-api-swagger-ui)
- [Endpoints da API](#-endpoints-da-api)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Suíte de Testes](#-suíte-de-testes)

---

## 🔍 Visão Geral
A aplicação evoluiu para um ambiente seguro, validado e documentado de ponta a ponta. A API permite gerenciar **Usuários**, **Roles (Papéis)** e **Posts**, garantindo que operações sensíveis sejam executadas apenas por usuários autenticados e com o nível de privilégio adequado.

### Principais Destaques:
- **Autenticação Stateless**: Utilização de tokens JWT via `Flask-JWT-Extended`.
- **RBAC Hierárquico**: Controle de autorização customizado com herança de permissões.
- **ORM Moderno**: Mapeamento objeto-relacional estruturado com `SQLAlchemy 2.0` (suporte a `Mapped` e `mapped_column`).
- **Serialização & Validação**: Utilização de `Marshmallow` integrada ao `Apispec`.
- **Documentação Interativa**: Swagger UI nativo integrado e gerado dinamicamente (`/docs`).
- **Migrações de Banco de Dados**: Versionamento com `Flask-Migrate` / `Alembic`.
- **Testes Automatizados**: Isolamento total de banco de dados em memória (`sqlite://`) e mocks unitários.

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.13+
- **Gerenciador de Dependências**: [Poetry](https://python-poetry.org/)
- **Framework Web**: Flask 3.x
- **ORM & Banco de Dados**: SQLAlchemy, Flask-SQLAlchemy, SQLite
- **Autenticação**: Flask-JWT-Extended (PyJWT)
- **Documentação**: Apispec, Flask-Swagger-UI
- **Serialização**: Marshmallow, Flask-Marshmallow
- **Migrações**: Flask-Migrate / Alembic
- **Testes**: Pytest, Unittest.Mock

---

## 📂 Arquitetura & Estrutura do Projeto

```text
api_flask/
├── migrations/                 # Scripts de migração de banco de dados (Alembic)
├── src/
│   ├── controllers/            # Blueprints / Endpoints da aplicação
│   │   ├── authcontroller.py   # Rota de Login e geração de Token JWT
│   │   ├── postcontroller.py   # CRUD de Posts
│   │   ├── rolecontroller.py   # CRUD de Roles
│   │   └── usercontroller.py   # CRUD de Usuários
│   ├── models/                 # Modelos de dados SQLAlchemy
│   │   ├── basemodel.py
│   │   ├── postmodel.py
│   │   ├── rolemodel.py
│   │   └── usermodel.py
│   ├── views/                  # Schemas do Marshmallow para serialização/validação
│   │   ├── postview.py
│   │   ├── roleview.py
│   │   └── userview.py
│   ├── app.py                  # Factory da aplicação Flask, extensões e Apispec
│   ├── config.py               # Configurações de ambiente (Dev, Test, Prod)
│   ├── utils.py                # Decoradores e funções utilitárias (RBAC)
│   └── wsgi.py                 # Ponto de entrada WSGI para produção
├── tests/
│   ├── integration/            # Testes de integração com banco em memória
│   │   ├── conftest.py         # Fixtures do Pytest (App context, client, tokens)
│   │   ├── test_post.py        # Testes dos endpoints de Posts
│   │   ├── test_role.py        # Testes dos endpoints de Roles
│   │   └── test_user.py        # Testes dos endpoints de Usuários
│   └── unit/                   # Testes unitários isolados
│       └── test_utils.py       # Testes de utilitários e decoradores com Mocks
├── pyproject.toml              # Configuração de dependências e metadados do Poetry
└── README.md                   # Documentação do projeto
```

## 🛡️ Controle de Acesso (RBAC)
A API adota um sistema de Acesso Baseado em Níveis Hierárquicos gerenciado pelo decorador customizado `@requires_role`:

```
Python

ROLE_NIVEL = {
    "visitante": 1,
    "normal": 2,
    "admin": 3
}
```

### 🎭 Papéis e Permissões:
1. __`visitante` (Nível 1)__: Possui acesso de apenas leitura. Pode listar e visualizar os posts, papéis e usuários da plataforma.

2. __`normal` (Nível 2)__: Herda os privilégios do visitante e ganha acesso total para criar, editar e excluir posts.

3. __`admin` (Nível 3)__: Acesso total e irrestrito. Gerencia criação, edição e remoção de usuários, papéis e posts.

## 📖 Documentação da API (Swagger UI)
A documentação interativa da API é gerada automaticamente através do docstrings YAML combinadas com os schemas do Marshmallow.
* Com a aplicação rodando, acesso a interface visual em: `http://127.0.0.1:5000/docs/`
* O arquivo JSON bruto da especificação OpenAPI fica disponível em: `http://127.0.0.1:5000/swagger.json`

## 📑 Endpoints da API
### 🔑 Autenticação (`/auth`)
|Método |Rota |Nível Mínimo |Descrição |
| --- | --- | --- | --- |
|`POST` |`/auth/login` |Público |Autentica um usuário e retorna o `access_token` JWT.|

### 👥 Usuários (`/users`)
|Método |Rota |Nível Mínimo |Descrição |
| --- | --- | --- | --- |
|`GET` |`/users/` |`visitante` |Lista todos os usuários cadastrados. |
|`GET` |`/users/<id>` |`admin` |Detalha as informações de um usuário. |
|`POST` |`/users/` |`admin` |Cadastra um novo usuário. |
|`PATCH` |`/users/<id>` |`admin` |Atualiza dados de um usuário existente. |
|`DELETE`|`/users/<id>` |`admin` |Remove um usuário do sistema. |

### 🛡️ Roles / Papéis (`/roles`)
|Método |Rota |Nível Mínimo |Descrição |
| --- | --- | --- | --- |
|`GET` |`/roles/` |`visitante` |Lista todas as roles cadastradas. |
|`POST` |`/roles/` |`admin` |Cadastra uma nova role. |
|`DELETE` |`/roles/<id>` |`admin` |Remove uma role do sistema. |

### 📝 Posts (`/posts`)
|Método |Rota |Nível Mínimo |Descrição |
| --- | --- | --- | --- |
|`GET` |`/posts/` |`visitante` |Lista todos os posts. |
|`GET` |`/posts/<id>` |`visitante` |Exibe os detalhes de um post especifico. |
|`POST` |`/posts/` |`normal` |Cria um novo post. |
|`PATCH` |`/posts/<id>` |`normal` |Atualiza o tilulo/conteúdo de um post. |
|`DELETE` |`/posts/<id>` |`normal` |Remove um post do sistema. |

## 🚀 Como Executar o Projeto
### Pré-requisitos
* __Python 3.13+__

* __Poetry instalado__

### 1. Clonar o repositório e instalar dependências
```
Bash

git clone <url-do-repositorio>
cd api_flask
poetry install
```

### 2. Inicializar o banco de dados
```
Bash

poetry run flask --app src.app run --debug
```

### 3. Executar o servidor de desenvolvimento
```
Bash

poetry run flask run
```

A API e o Swagger UI estarão acessíveis em `http://127.0.0.1:5000/docs/`.

### 🧪 Suíte de Testes
Os testes são executados com Pytest utilizando um banco SQLite isolado em memória (`sqlite://`), garantindo rapidez e consistência sem poluir o banco de dados local.

#### Rodar todos os testes (Unitários e Integração)
```
Bash

poetry run pytest tests
```

#### Rodar apenas os testes de integração
```
Bash

poetry run pytest tests/integration
```

#### Rodar apenas os testes unitários
```
Bash

poetry run pytest tests/unit
```
__Projeto desenvolvido como parte do treinamento e aprimoramento em APIs RESTful com Python.__