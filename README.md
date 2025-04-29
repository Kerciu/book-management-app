# Book Collection Manager 🏷️

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Leptos](https://img.shields.io/badge/Leptos-0.1.0-blue?style=for-the-badge)](https://leptos.dev/)

A web application for managing book collections, reviewing books, and sharing recommendations with friends.

## ✨ Features

- **📚 Personal Library** - Create and organize collections of read, currently reading, and planned books
- **⭐ Reviews & Ratings** - Share detailed thoughts and rate books (1-5 stars)
- **📖 Reading Progress** - Track current page/chapter and reading status
- **👥 Social Sharing** - Recommend books to friends and view their collections
- **🔍 Smart Discovery** - Advanced search for books/authors with filters
- **🎯 AI Recommendations** - Personalized suggestions based on your reading history
- **🔒 Secure Auth** - JWT and OAuth (Google/GitHub) authentication

## 🛠️ Tech Stack

| Component        | Technology                          |
|------------------|-------------------------------------|
| **Backend**      | Django REST Framework               |
| **Frontend**     | Leptos (Rust WASM framework)        |
| **Database**     | PostgreSQL 15                       |
| **Container**    | Docker + Docker Compose             |
| **Auth**         | JWT Tokens + OAuth 2.0              |
| **CI/CD**        | GitHub Actions (if applicable)      |

## 🚀 Getting Started

### Prerequisites
- Docker Engine ≥ 20.10
- Docker Compose V2
- Make (optional)

### Installation & Setup
```bash
# Initialize and start all services
$ make init
```
### Makefile commands
  - `make backend_logs` - returns logs from backend container
  - `make runserver` - runs app on 0.0.0.0:8000
  - `make makemigrations` - runs django makemigrations command
  - `make migrate` - runs django migrate command
  - `make docker_run argument="$(argument)"` - runs django command specified by argument
