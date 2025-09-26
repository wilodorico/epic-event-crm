from enum import Enum, auto


class Permissions(Enum):
    CREATE_COLLABORATOR = auto()
    UPDATE_COLLABORATOR = auto()
    DELETE_COLLABORATOR = auto()
    CREATE_CUSTOMER = auto()
    UPDATE_CUSTOMER = auto()
    READ_CUSTOMERS = auto()
    CREATE_CONTRACT = auto()
    UPDATE_CONTRACT = auto()
    READ_CONTRACTS = auto()
