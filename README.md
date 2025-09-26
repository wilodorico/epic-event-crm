






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