import datetime

from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC
from collaborators.domain.event.event import Event
from collaborators.domain.event.event_repository_abc import EventRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateEventUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryABC,
        contract_repository: ContractRepositoryABC,
        id_generator: IdGeneratorABC,
        auth_context: AuthContextABC,
    ):
        self._event_repository = event_repository
        self._contract_repository = contract_repository
        self._id_generator = id_generator
        self._auth_context = auth_context

    def execute(
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
        self._auth_context.ensure(Permissions.CREATE_EVENT)

        event_id = self._id_generator.generate()
        contract = self._contract_repository.find_by_id(contract_id)

        if contract is None:
            raise ValueError("Contract not found")

        if not contract.is_signed():
            raise ValueError("Contract must be signed to create an event")

        if contract.commercial_id != creator.id:
            raise PermissionError("You do not have permission to create an event for this contract")

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
