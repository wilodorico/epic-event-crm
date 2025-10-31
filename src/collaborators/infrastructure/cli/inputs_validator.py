import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

import click


def validate_email(ctx, param, value):
    """Validate that the input is a valid email address."""
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, value):
        raise click.BadParameter("Invalid email address")
    return value


def validate_phone(ctx, param, value):
    """Validate that the input is a valid phone number."""
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


def validate_date_start(ctx, param, value):
    """Callback to store date_start in context for later validation."""
    if value:
        # Check if date_start is in the future
        if value <= datetime.now():
            raise click.BadParameter("Event start date must be in the future. Please enter a future date.")

        # Store date_start in context for date_end validation
        if not hasattr(ctx, "meta"):
            ctx.meta = {}
        ctx.meta["date_start"] = value
    return value


def validate_date_end(ctx, param, value):
    """Callback to validate that date_end is after date_start."""
    if value and hasattr(ctx, "meta") and "date_start" in ctx.meta:
        date_start = ctx.meta["date_start"]
        if value <= date_start:
            raise click.BadParameter("Event end date must be after start date. Please enter a future date.")
    return value
