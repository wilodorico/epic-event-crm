"""Sentry configuration and initialization module.

This module handles the setup and configuration of Sentry for error tracking
and performance monitoring. It loads configuration from environment variables
and provides a centralized way to manage Sentry integration.
"""

import os
from typing import Optional

import sentry_sdk
from dotenv import load_dotenv


def init_sentry() -> None:
    """Initializes Sentry SDK with configuration from environment variables.

    Reads Sentry configuration from .env file and initializes the SDK if enabled.
    This should be called once at application startup.

    Environment Variables:
        SENTRY_DSN: The Sentry Data Source Name (required if enabled).
        SENTRY_ENABLED: Whether to enable Sentry (default: true).
        SENTRY_ENVIRONMENT: The environment name (default: development).
        SENTRY_TRACES_SAMPLE_RATE: Performance monitoring sample rate (default: 1.0).

    Note:
        If SENTRY_ENABLED is false or SENTRY_DSN is not set, Sentry will not be initialized.
        This allows local development without requiring Sentry configuration.
    """
    load_dotenv()

    sentry_enabled = os.getenv("SENTRY_ENABLED", "true").lower() == "true"
    sentry_dsn: Optional[str] = os.getenv("SENTRY_DSN")

    if not sentry_enabled:
        print("ℹ️  Sentry is disabled (SENTRY_ENABLED=false)")
        return

    if not sentry_dsn:
        print("⚠️  Sentry DSN not configured. Sentry will not be initialized.")
        print("   Set SENTRY_DSN in your .env file to enable error tracking.")
        return

    environment = os.getenv("SENTRY_ENVIRONMENT", "development")
    traces_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))

    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=environment,
        traces_sample_rate=traces_sample_rate,
        # Enable automatic breadcrumbs
        integrations=[],
        # Send default PII (Personally Identifiable Information)
        send_default_pii=False,
        # Attach stack trace to messages
        attach_stacktrace=True,
    )

    print(f"✅ Sentry initialized (environment: {environment})")


def capture_message(message: str, level: str = "info", **extra) -> None:
    """Captures a message in Sentry with optional extra context.

    Args:
        message: The message to log.
        level: The severity level (debug, info, warning, error, fatal).
        **extra: Additional context data to attach to the message.

    Note:
        If Sentry is not initialized, this function will silently do nothing.
    """
    sentry_sdk.capture_message(message, level=level)
    if extra:
        sentry_sdk.set_context("extra", extra)


def capture_exception(exception: Exception, **extra) -> None:
    """Captures an exception in Sentry with optional extra context.

    Args:
        exception: The exception to capture.
        **extra: Additional context data to attach to the exception.

    Note:
        If Sentry is not initialized, this function will silently do nothing.
    """
    if extra:
        sentry_sdk.set_context("extra", extra)
    sentry_sdk.capture_exception(exception)


def set_user_context(user_id: str, email: Optional[str] = None, role: Optional[str] = None) -> None:
    """Sets user context for Sentry events.

    Args:
        user_id: The unique identifier of the user.
        email: The user's email address (optional).
        role: The user's role (optional).

    Note:
        This context will be attached to all subsequent Sentry events until cleared.
    """
    sentry_sdk.set_user({"id": user_id, "email": email, "role": role})


def clear_user_context() -> None:
    """Clears the user context in Sentry.

    Call this when a user logs out or when you want to stop associating
    events with a specific user.
    """
    sentry_sdk.set_user(None)
