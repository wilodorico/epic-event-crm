class AuthorizationError(PermissionError):
    """Exception raised when a user lacks the necessary permissions."""

    def __init__(self, user, permission):
        message = f"User '{user.email}' with role '{user.role.value}' does not have permission '{permission.name}'"
        super().__init__(message)
