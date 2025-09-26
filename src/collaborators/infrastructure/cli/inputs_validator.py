import re
from decimal import Decimal, InvalidOperation

import click


def validate_email(ctx, param, value):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, value):
        raise click.BadParameter("Invalid email address")
    return value


def validate_phone(ctx, param, value):
    phone_regex = r"^\d{10}$"  # Exemple : numéro français à 10 chiffres
    if not re.match(phone_regex, value):
        raise click.BadParameter("Invalid phone number (10 digits expected)")
    return value


def validate_positive_decimal(ctx, param, value):
    """Validate that the input is a positive decimal number."""
    try:
        decimal_value = Decimal(value)
        if decimal_value < 0:
            raise click.BadParameter("Value must be a positive decimal number")
    except (ValueError, TypeError, InvalidOperation):
        raise click.BadParameter("Value must be a valid decimal number")
    return value
