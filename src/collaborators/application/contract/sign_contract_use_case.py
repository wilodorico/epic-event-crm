from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC
from collaborators.infrastructure.sentry_config import capture_message


class SignContractUseCase(UseCaseABC):
    """Handles the signing of a contract by an authorized user.

    This use case ensures that only authorized users can sign contracts. It validates
    the contract's existence, checks that it has not been signed already, marks it as
    signed, and persists the updated contract in the repository.

    Requires the SIGN_CONTRACT permission to execute.
    """

    permissions = Permissions.SIGN_CONTRACT

    def __init__(self, auth_context: AuthContextABC, repository: ContractRepositoryABC):
        super().__init__(auth_context)
        self.repository = repository

    def _execute(self, updater_id: str, contract_id: str) -> None:
        """Signs a contract.

        Args:
            updater_id: The unique identifier of the collaborator signing the contract.
            contract_id: The unique identifier of the contract to sign.

        Raises:
            ValueError: If the contract is not found or is already signed.
            PermissionError: If the user lacks permissions.

        Returns:
            None. The contract is marked as signed and persisted in the repository.
        """
        contract = self.repository.find_by_id(contract_id)
        if not contract:
            raise ValueError("Contract not found.")

        if contract.is_signed():
            raise ValueError("Contract is already signed.")

        contract.sign_contract(updater_id)

        self.repository.update(contract)

        # Log contract signature to Sentry
        capture_message(
            f"Contract signed: {contract_id}",
            level="info",
            contract_id=contract_id,
            customer_id=contract.customer_id,
            commercial_id=contract.commercial_id,
            total_amount=str(contract.total_amount),
            signed_by=updater_id,
        )
