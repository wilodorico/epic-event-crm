from datetime import datetime

from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC
from collaborators.domain.event.event import Event
from collaborators.domain.event.event_repository_abc import EventRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateEventUseCase(UseCaseABC):
    """Handles the creation of a new event by a commercial contact.

    This use case ensures that only the commercial contact assigned to a signed contract
    can create events. It validates the contract's existence and signature status, checks
    date consistency, and saves the new event record to the repository.

    Requires the CREATE_EVENT permission to execute.
    """

    permissions = Permissions.CREATE_EVENT

    def __init__(
        self,
        auth_context: AuthContextABC,
        event_repository: EventRepositoryABC,
        contract_repository: ContractRepositoryABC,
        id_generator: IdGeneratorABC,
    ):
        super().__init__(auth_context)
        self._event_repository = event_repository
        self._contract_repository = contract_repository
        self._id_generator = id_generator

    def _execute(
        self,
        creator: Collaborator,
        title: str,
        contract_id: str,
        date_start: datetime,
        date_end: datetime,
        location: str,
        attendees: int,
        notes: str,
    ) -> Event:
        """Creates and persists a new event entity.

        Args:
            creator: The collaborator performing the operation.
            title: The event's title.
            contract_id: The unique identifier of the signed contract.
            date_start: The event's start date and time.
            date_end: The event's end date and time.
            location: The event's physical location.
            attendees: The expected number of attendees.
            notes: Additional notes or instructions for the event.

        Raises:
            ValueError: If the contract is not found, not signed, if dates are invalid
                (end before start or start in the past).
            PermissionError: If the user lacks permissions or attempts to create an event
                for a contract not assigned to them.

        Returns:
            Event: The newly created event entity linked to the contract and customer.
        """
        event_id = self._id_generator.generate()
        contract = self._contract_repository.find_by_id(contract_id)

        if contract is None:
            raise ValueError("Contract not found")

        if not contract.is_signed():
            raise ValueError("Contract must be signed to create an event")

        if contract.commercial_id != creator.id:
            raise PermissionError("You do not have permission to create an event for this contract")

        if date_end <= date_start:
            raise ValueError("Event end date must be after start date")

        if date_start < datetime.now():
            raise ValueError("Event start date must be in the future")

        event = Event(
            id=event_id,
            title=title,
            customer_id=contract.customer_id,
            contract_id=contract_id,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )

        self._event_repository.create(event)

        return event
