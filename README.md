# 🚀 Flask REST API - RBAC & Automated Testing

Uma API REST profissional, robusta e desenvolvida em Python/Flask, com autenticação JWT, controle de acesso baseado em papéis hierárquicos (RBAC) e uma suíte completa de testes automatizados (unitários e de integração).

---

## 📌 Sumário
- [Visão Geral](#-visão-geral)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura & Estrutura do Projeto](#-arquitetura--estrutura-do-projeto)
- [Controle de Acesso (RBAC)](#-controle-de-acesso-rbac)
- [Endpoints da API](#-endpoints-da-api)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Suíte de Testes](#-suíte-de-testes)

---

## 🔍 Visão Geral
A aplicação evoluiu de um protótipo inicial para um ambiente de produção seguro com controle estrito de permissões. A API permite gerenciar **Usuários**, **Roles (Papéis)** e **Posts**, garantindo que operações sensíveis sejam executadas apenas por usuários com o nível de privilégio adequado.

### Principais Destaques:
- **Autenticação Stateless**: Utilização de tokens JWT via `Flask-JWT-Extended`.
- **RBAC Hierárquico**: Controle de autorização customizado com herança de permissões.
- **ORM Moderno**: Mapeamento objeto-relacional estruturado com `SQLAlchemy 2.0` (suporte a `Mapped` e `mapped_column`).
- **Migrações de Banco de Dados**: Versionamento com `Flask-Migrate` / `Alembic`.
- **Testes Automatizados**: Isolamento total de banco de dados em memória (`sqlite://`) e mocks unitários.

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.13+
- **Gerenciador de Dependências**: [Poetry](https://python-poetry.org/)
- **Framework Web**: Flask 3.x
- **ORM & Banco de Dados**: SQLAlchemy, Flask-SQLAlchemy, SQLite
- **Autenticação**: Flask-JWT-Extended (PyJWT)
- **Migrações**: Flask-Migrate / Alembic
- **Testes**: Pytest, Unittest.Mock

---

## 📂 Arquitetura & Estrutura do Projeto

```text
api_flask/
├── migrations/          # Scripts de migração de banco de dados (Alembic)
├── src/
│   ├── controllers/     # Blueprints / Rotas da aplicação
│   │   ├── authcontroller.py   # Rota de Login e geração de Token
│   │   ├── postcontroller.py   # CRUD de Posts
│   │   ├── rolecontroller.py   # CRUD de Roles
│   │   └── usercontroller.py   # CRUD de Usuários
│   ├── app.py           # Factory da aplicação Flask e modelos SQLAlchemy
│   ├── db.py            # Inicialização e contexto do banco de dados
│   ├── schema.sql       # Script SQL inicial (caso aplicável)
│   └── utils.py         # Decoradores e funções auxiliares (RBAC)
├── tests/
│   ├── integration/     # Testes de integração (Com banco de dados em memória)
│   │   ├── conftest.py  # Fixtures do Pytest (App context, client, tokens)
│   │   ├── test_role.py # Testes dos endpoints de Roles
│   │   └── test_user.py # Testes dos endpoints de Usuários
│   └── unit/            # Testes unitários isolados
│       └── test_utils.py # Testes de utilitários e decoradores com Mocks
├── pyproject.toml       # Configuração de dependências e metadados do Poetry
└── README.md            # Documentação do projeto
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

poetry run flask init-db
```

### 3. Executar o servidor de desenvolvimento
```
Bash

poetry run flask run
```

A API estará acessível em `http://127.0.0.1:5000`.

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