






## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)

For error tracking and monitoring with Sentry:

```bash
cp .env.example .env
# Edit .env and add your Sentry DSN
```

See [SENTRY_SETUP.md](SENTRY_SETUP.md) for detailed Sentry configuration instructions.

**Note**: The application works without Sentry configuration. If no `.env` file is provided or `SENTRY_ENABLED=false`, the application will run normally without error tracking.

### 3. Initialize Database

```bash
make init-db
# or
python src/app.py init-db
```

## Features

- ✅ Role-based access control (Management, Commercial, Support)
- ✅ Collaborator management (CRUD operations)
- ✅ Customer management
- ✅ Contract management with signing workflow
- ✅ Event management with support assignment
- ✅ Secure authentication with JWT
- ✅ Error tracking and monitoring with Sentry (optional)
- ✅ Comprehensive audit logging

## Cli commands
```
init-db // initialize the database
collaborator create-collaborator
collaborator update-collaborator --id "collaborator_id"
collaborator delete-collaborator --id "collaborator_id"

customer create-customer
customer update-customer --id "customer_id"
customer get-customers

contract create-contract --id "customer_id"
contract update-contract --id "contract_id"
contract get-contracts

```

## make commands
```
make help -> to see all command bash
```


## Faire la vérification des tests e2e avec les commands cli
```
au lieu de faire ça :
    repo = SqlalchemyCollaboratorRepository(session)
    assert repo.find_by_email("wrong-email") is None

on va faire : 
collaborators = cli.get_collaborators 
assert 0
```