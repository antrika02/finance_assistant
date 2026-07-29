# FinPilot AI

**A production-oriented personal finance AI backend built with FastAPI, PostgreSQL, SQLAlchemy, and Clean Architecture.**

Status: 🚧 Active Development

## Overview

FinPilot AI is a backend system evolving into an AI-powered personal finance assistant. Rather than a simple CRUD app, it's built as an enterprise-grade service following clean architecture principles, and will eventually support:

- Transaction, budget, and savings tracking
- Credit card and reward point management
- AI-powered financial insights via LLMs
- Retrieval-Augmented Generation (RAG) over financial data
- Conversational memory using LangGraph

## Architecture

```
Client
  │
  ▼
FastAPI Router
  │
  ▼
Dependency Injection
  │
  ▼
Service Layer
  │
  ▼
Repository Layer
  │
  ▼
SQLAlchemy ORM
  │
  ▼
PostgreSQL
```

## Tech Stack

| Layer | Tools |
|---|---|
| Language / Framework | Python 3.12, FastAPI |
| Database | PostgreSQL, SQLAlchemy 2.x, Alembic |
| Configuration | Pydantic Settings, python-dotenv |
| Logging | Loguru |
| Tooling | Docker, pgAdmin, uv, Git |

## Project Structure

```
personal_finance_agent/
├── alembic/versions/          # DB migrations
├── app/
│   ├── api/                   # Routers, versioned endpoints
│   ├── core/                  # App factory, settings, logging
│   ├── database/               # Session management
│   ├── dependencies/           # DI providers
│   ├── models/                 # ORM models
│   ├── repositories/            # Data access layer
│   ├── services/                # Business logic layer
│   ├── graph/                   # LangGraph agent graphs
│   ├── memory/                  # Conversational memory
│   ├── prompts/                 # LLM prompt templates
│   ├── tools/                   # Agent tool calling
│   └── utils/
├── docker/
├── docs/
└── README.md
```

## Current API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| POST | `/users` | Create a user |
| GET | `/users` | List all users |
| GET | `/users/{id}` | Retrieve a user by ID |

## Database

**Current tables:** `users`, `alembic_version`

**Planned tables:** `transactions`, `credit_cards`, `reward_points`, `budgets`, `categories`, `savings_goals`, `chat_history`

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd personal_finance_agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment

Create a `.env` file in the project root:

```env
APP_NAME=FinPilot AI
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=True

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=personal_finance
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

### 4. Start PostgreSQL

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 5. Run database migrations

```bash
uv run alembic upgrade head
```

### 6. Start the API

```bash
uv run uvicorn app.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| 1 | Project setup, Docker, PostgreSQL, SQLAlchemy, Alembic, User module | ✅ Complete |
| 2 | Generic repository/service, exception handling, CRUD improvements | 🚧 In Progress |
| 3 | Transactions, budgets, credit cards, reward points | 📅 Planned |
| 4 | Authentication, authorization, user preferences | 📅 Planned |
| 5 | LangGraph agent, Claude API, tool calling, memory, RAG | 📅 Planned |
| 6 | Streamlit dashboard, analytics, deployment, CI/CD, observability | 📅 Planned |

### In Progress

- Generic base repository & service
- Custom exception handling and global error handlers
- Timestamp mixins
- Request/response logging

## Learning Goals

This project is a hands-on exploration of:

- Clean Architecture and SOLID principles
- Repository and Service Layer patterns
- Dependency Injection
- Database migrations at scale
- Enterprise-grade FastAPI development
- AI agent development (LangGraph, RAG, tool calling)
- Production backend engineering practices

## License

This project is under active development. License to be determined.
