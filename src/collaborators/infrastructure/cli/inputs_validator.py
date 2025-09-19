import re

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
