class AuthorizationError(PermissionError):
    """Exception raised for authorization errors."""

    def __init__(self, user, permission):
        message = f"User '{user.email}' with role '{user.role.value}' does not have permission '{permission.name}'"
        super().__init__(message)
