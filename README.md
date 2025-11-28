# 🎯 Epic Events CRM

> A secure, role-based Customer Relationship Management (CRM) system for event management company Epic Events.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-Passing-success.svg)](tests/)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Role-Based Permissions](#role-based-permissions)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [CLI Commands](#cli-commands)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Documentation](#documentation)

---

## 🎯 Overview

Epic Events CRM is a command-line application designed to manage customers, contracts, and events for an event management company. The system implements a robust **role-based access control (RBAC)** system with three distinct user roles, ensuring secure and appropriate access to business operations.

### Key Objectives

- Secure management of collaborators, customers, contracts, and events
- Role-based permissions (Management, Commercial, Support)
- Complete audit trail with Sentry integration
- Clean Architecture implementation for maintainability
- Comprehensive test coverage (unit, integration, e2e)

---

## ✨ Features

### 👥 User Management
- ✅ Create, update, and delete collaborators
- ✅ Three role types: Management, Commercial, Support
- ✅ Secure authentication with JWT tokens
- ✅ Session persistence across CLI commands

### 👤 Customer Management
- ✅ Commercial contacts create and manage their customers
- ✅ Track customer information (name, email, company, phone)
- ✅ Link customers to their assigned commercial representative

### 📄 Contract Management
- ✅ Create contracts for customers (Management only)
- ✅ Track total and remaining amounts
- ✅ Sign contracts (prerequisite for event creation)
- ✅ Filter by unsigned contracts or unpaid contracts
- ✅ Commercial can only update their own contracts

### 🎉 Event Management
- ✅ Create events from signed contracts (Commercial only)
- ✅ Assign support contacts to events (Management only)
- ✅ Support can update their assigned events
- ✅ Filter unassigned events
- ✅ Prevent updates to past events

### 🔒 Security & Monitoring
- ✅ Role-based access control (RBAC)
- ✅ JWT authentication with secure sessions
- ✅ Password hashing with bcrypt
- ✅ Sentry integration for error tracking and audit logging
- ✅ Environment-based configuration (no secrets in code)

---

## 🏗️ Architecture

This project follows **Clean Architecture** principles, separating concerns into distinct layers:

```
┌─────────────────────────────────────────────────┐
│          Infrastructure Layer                    │
│  (CLI, Database, External Services, Sentry)     │
├─────────────────────────────────────────────────┤
│          Application Layer                       │
│  (Use Cases, Services, Permissions)             │
├─────────────────────────────────────────────────┤
│          Domain Layer                            │
│  (Entities, Business Rules, Repositories)       │
└─────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### 🔷 Domain Layer (`domain/`)
**Core business logic, independent of external concerns**
- **Entities**: `Collaborator`, `Customer`, `Contract`, `Event`
- **Value Objects**: `Role`, `ContractStatus`, `Permissions`
- **Repository Interfaces**: Define contracts for data access
- **Business Rules**: Validation, entity methods

#### 🔶 Application Layer (`application/`)
**Orchestrates business use cases**
- **Use Cases**: One per business operation (e.g., `CreateCollaboratorUseCase`)
- **Services**: `AuthContext` (permission checking), `PasswordHasher`
- **DTOs**: `CollaboratorUpdateData`, `ContractUpdateData`, etc.
- **Exceptions**: Domain-specific errors

#### 🔴 Infrastructure Layer (`infrastructure/`)
**Technical implementation details**
- **CLI**: Click-based command-line interface
- **Database**: SQLAlchemy repositories and models
- **Security**: JWT token management, bcrypt password hashing
- **Monitoring**: Sentry configuration and integration
- **Mappers**: Convert between domain entities and database models

### Design Patterns Used

- **Repository Pattern**: Abstract data access
- **Dependency Injection**: Decouple components
- **Use Case Pattern**: Encapsulate business operations

---

## 🔐 Role-Based Permissions

The system implements fine-grained role-based access control:

### 👔 Management Role

**Collaborator Management:**
- ✅ Create collaborators
- ✅ Update collaborators
- ✅ Delete collaborators

**Contract Management:**
- ✅ Create contracts
- ✅ Update contracts
- ✅ Sign contracts
- ✅ Read all contracts

**Event Management:**
- ✅ Assign support to events
- ✅ Read all events
- ✅ Filter unassigned events

**Customer Access:**
- ✅ Read all customers

### 💼 Commercial Role

**Customer Management:**
- ✅ Create customers (automatically assigned to them)
- ✅ Update their own customers

**Contract Management:**
- ✅ Update their own contracts
- ✅ Sign contracts
- ✅ Read all contracts
- ✅ Filter unsigned/unpaid contracts

**Event Management:**
- ✅ Create events for their signed contracts
- ✅ Read all events

### 🛠️ Support Role

**Event Management:**
- ✅ Update their assigned events
- ✅ Cannot update past events
- ✅ Read all events

**Read-Only Access:**
- ✅ View customers
- ✅ View contracts

### Permission Matrix

| Operation | Management | Commercial | Support |
|-----------|-----------|-----------|---------|
| Create Collaborator | ✅ | ❌ | ❌ |
| Update Collaborator | ✅ | ❌ | ❌ |
| Delete Collaborator | ✅ | ❌ | ❌ |
| Create Customer | ✅ (read-only)| ✅ | ❌ |
| Update Customer | ✅ (read-only)| ✅ (own) | ❌ |
| Create Contract | ✅ | ❌ | ❌ |
| Update Contract | ✅ | ✅ (own) | ❌ |
| Sign Contract | ✅ | ✅ | ❌ |
| Create Event | ❌ | ✅ | ❌ |
| Assign Support to Event | ✅ | ❌ | ❌ |
| Update Event | ❌ | ❌ | ✅ (assigned) |
| Read All Data | ✅ | ✅ (limited) | ✅ (read-only) |

---

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/wilodorico/epic-event-crm.git
   cd epic-event-crm
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python src/app.py init-db
   ```

5. **Verify installation**
   ```bash
   python src/app.py --help
   ```

---

## ⚙️ Configuration

### Environment Variables (Optional)

For error tracking and monitoring with Sentry:

1. **Copy the example file**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and configure Sentry**
   ```env
   SENTRY_DSN=https://your-dsn@sentry.io/your-project-id
   SENTRY_ENVIRONMENT=development
   SENTRY_ENABLED=true
   SENTRY_TRACES_SAMPLE_RATE=1.0
   ```

**Note:** The application works perfectly without Sentry configuration. Sentry is optional for local development.

---

## 🚀 Usage

### Basic Workflow

1. **Initialize database** (first time only)
   ```bash
   python src/app.py init-db
   ```

2. **Login as a collaborator**
   ```bash
   python src/app.py auth login
   ```

3. **Execute commands based on your role**
   ```bash
   # Example: Create a customer (Commercial role)
   python src/app.py customer create-customer

   # Example: Create a contract (Management role)
   python src/app.py contract create-contract --customer-id <id>
   ```

4. **Logout**
   ```bash
   python src/app.py auth logout
   ```

---

## 📝 CLI Commands

### Authentication Commands

```bash
# Login
python src/app.py auth login

# Logout
python src/app.py auth logout
```

### Collaborator Commands (Management only)

```bash
# Create a collaborator
python src/app.py collaborator create-collaborator

# Update a collaborator
python src/app.py collaborator update-collaborator --id <collaborator_id>

# Delete a collaborator
python src/app.py collaborator delete-collaborator --id <collaborator_id>
```

### Customer Commands

```bash
# Create a customer (Commercial)
python src/app.py customer create-customer

# Update a customer (Commercial - own only)
python src/app.py customer update-customer --id <customer_id>

# List all customers
python src/app.py customer get-customers
```

### Contract Commands

```bash
# Create a contract (Management)
python src/app.py contract create-contract --customer-id <customer_id>

# Update a contract (Management or Commercial - own)
python src/app.py contract update-contract --id <contract_id>

# Sign a contract (Management or Commercial)
python src/app.py contract sign-contract --id <contract_id>

# List all contracts
python src/app.py contract get-contracts

# List unsigned contracts
python src/app.py contract get-unsigned-contracts

# List unpaid contracts
python src/app.py contract get-unpaid-contracts
```

### Event Commands

```bash
# Create an event (Commercial - from signed contract)
python src/app.py event create --contract-id <contract_id>

# Assign support to event (Management)
python src/app.py event assign-support --event-id <event_id> --support-id <support_id>

# Update assigned event (Support - own only)
python src/app.py event update-assigned-event --id <event_id>

# List all events
python src/app.py event get-events

# List unassigned events (Management)
python src/app.py event get-unassigned-events

# List support's assigned events (Support)
python src/app.py event get-my-events
```

### Database Management

```bash
# Initialize database
python src/app.py init-db
```

---

## 🧪 Testing

The project includes comprehensive test coverage across three levels:

### Test Structure

```
src/collaborators/tests/
├── conftest.py              # Shared test fixtures
├── fakes/                   # In-memory test repositories
├── services/                # Service layer tests
├── usecases/               # Use case unit tests
│   ├── collaborator/
│   ├── contract/
│   ├── customer/
│   └── event/
└── e2e/                    # End-to-end CLI tests
    ├── auth/
    ├── collaborator/
    ├── contract/
    ├── customer/
    └── event/
```

### Running Tests

#### Using Makefile (Recommended)

```bash
# Show available commands
make help

# Run unit tests (with fake repositories)
make test

# Run integration tests (with SQLAlchemy)
make integration

# Run end-to-end tests (with real database)
make e2e

# Run all tests
make all
```

#### Using pytest directly

```bash
# Unit tests only
cd src && pytest

# Integration tests
cd src && USE_SQLALCHEMY_REPO=1 pytest collaborators/tests/usecases

# E2E tests
cd src && USE_SQLALCHEMY_REPO=1 pytest collaborators/tests/e2e

# All tests with verbose output
cd src && USE_SQLALCHEMY_REPO=1 pytest -vvv collaborators/tests
```

### Test Coverage

- **Unit Tests**: Test use cases with fake repositories (fast, isolated)
- **Integration Tests**: Test use cases with real database (SQLAlchemy)
- **E2E Tests**: Test complete workflows through CLI commands

---

## 📁 Project Structure

```
epic-event-crm/
├── src/
│   ├── app.py                          # Application entry point
│   ├── collaborators/
│   │   ├── application/                # Application layer
│   │   │   ├── collaborator/          # Collaborator use cases
│   │   │   ├── contract/              # Contract use cases
│   │   │   ├── customer/              # Customer use cases
│   │   │   ├── event/                 # Event use cases
│   │   │   ├── exceptions/            # Custom exceptions
│   │   │   ├── services/              # Application services
│   │   │   │   ├── auth_context.py   # Permission checking
│   │   │   │   └── auth_context_abc.py
│   │   │   └── use_case_abc.py        # Base use case class
│   │   ├── domain/                     # Domain layer
│   │   │   ├── collaborator/
│   │   │   │   ├── collaborator.py   # Collaborator entity
│   │   │   │   ├── permissions.py    # Permission enum
│   │   │   │   └── collaborator_repository_abc.py
│   │   │   ├── contract/
│   │   │   │   ├── contract.py       # Contract entity
│   │   │   │   └── contract_repository_abc.py
│   │   │   ├── customer/
│   │   │   │   ├── customer.py       # Customer entity
│   │   │   │   └── customer_repository_abc.py
│   │   │   └── event/
│   │   │       ├── event.py          # Event entity
│   │   │       └── event_repository_abc.py
│   │   ├── infrastructure/             # Infrastructure layer
│   │   │   ├── cli/                   # CLI interface (Click)
│   │   │   │   ├── commands/         # Command implementations
│   │   │   │   │   ├── auth/
│   │   │   │   │   ├── collaborator/
│   │   │   │   │   ├── contract/
│   │   │   │   │   ├── customer/
│   │   │   │   │   ├── event/
│   │   │   │   │   └── init_db.py
│   │   │   │   ├── decorators.py     # CLI decorators
│   │   │   │   └── inputs_validator.py
│   │   │   ├── database/             # SQLAlchemy setup
│   │   │   ├── mappers/              # Entity/Model mappers
│   │   │   ├── repositories/         # SQLAlchemy repositories
│   │   │   ├── security/             # JWT, password hashing
│   │   │   └── sentry_config.py      # Sentry integration
│   │   └── tests/                     # Test suite
│   │       ├── conftest.py
│   │       ├── fakes/                # Fake repositories
│   │       ├── services/
│   │       ├── usecases/             # Unit tests
│   │       └── e2e/                  # E2E tests
│   └── commons/                       # Shared utilities
│       ├── id_generator_abc.py
│       └── uuid_generator.py
├── .env.example                       # Environment template
├── .gitignore
├── Makefile                           # Test commands
├── pyproject.toml                     # Project configuration
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
└── test_sentry.py                     # Sentry test script
```

---

## 🛠️ Technologies

### Core Technologies

- **Python 3.12**: Programming language
- **Click 8.2**: CLI framework
- **SQLAlchemy 2.0**: ORM for database interactions
- **SQLite**: Database (development)

### Security

- **bcrypt 5.0**: Password hashing
- **PyJWT 2.10**: JSON Web Token authentication

### Monitoring & Logging

- **Sentry SDK 2.18**: Error tracking and monitoring
- **python-dotenv 1.0**: Environment variable management

### Testing

- **pytest 8.4**: Testing framework
- **Fake repositories**: In-memory test doubles

### Code Quality

- **Ruff**: Fast Python linter and formatter
- **Type hints**: Enhanced code reliability

---

## 📚 Documentation

### Code Documentation

All classes and methods include comprehensive **Google Style docstrings** with:
- Clear descriptions of purpose and functionality
- Parameter documentation with types and descriptions
- Return value documentation
- Exception documentation for error cases
- Usage examples where applicable

### Sentry Integration

**Error Tracking & Monitoring:**

The application integrates Sentry for production-grade error tracking and business event logging.

**Configuration:**
1. Create a `.env` file from `.env.example`
2. Add your Sentry DSN (get it from https://sentry.io)
3. Set `SENTRY_ENABLED=true` to activate

**Testing:**
```bash
python test_sentry.py
```

This script will:
- Initialize Sentry with your configuration
- Send a test message
- Send a test exception
- Provide feedback on the configuration status

**Security:**
- DSN stored in environment variables (never in code)
- `.env` file excluded from version control
- Optional for local development

### Audit Logging

The following operations are automatically logged to Sentry:

- ✅ All unexpected exceptions (automatic)
- ✅ Collaborator creation
- ✅ Collaborator modification
- ✅ Collaborator deletion
- ✅ Contract signature

---

## 👤 Author

**Wilfried Odorico**
- GitHub: [@wilodorico](https://github.com/wilodorico)

---

**Made with ❤️ for Epic Events**