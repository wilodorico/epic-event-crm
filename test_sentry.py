"""
Test script to verify Sentry integration.

This script performs the following checks:
1. Verifies Sentry configuration
2. Sends a test message
3. Sends a test exception

Run this script after configuring your .env file to ensure Sentry is working.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from collaborators.infrastructure.sentry_config import capture_exception, capture_message, init_sentry


def test_sentry_integration():
    """Tests Sentry integration by sending test events."""

    print("=" * 60)
    print("Sentry Integration Test")
    print("=" * 60)
    print()

    # Initialize Sentry
    print("1. Initializing Sentry...")
    init_sentry()
    print()

    # Test message capture
    print("2. Sending test message to Sentry...")
    capture_message(
        "Sentry test message from Epic Events CRM",
        level="info",
        test=True,
        environment="test",
    )
    print("✅ Test message sent")
    print()

    # Test exception capture
    print("3. Sending test exception to Sentry...")
    try:
        # Intentionally raise an exception
        raise ValueError("This is a test exception for Sentry integration")
    except Exception as e:
        capture_exception(e, test=True, source="sentry_test_script")
        print("✅ Test exception sent")
    print()

    print("=" * 60)
    print("Test completed!")
    print()
    print("Check your Sentry dashboard at https://sentry.io")
    print("You should see:")
    print("  - A test message in the 'Issues' section")
    print("  - A ValueError in the 'Issues' section")
    print()
    print("If you don't see events, check:")
    print("  1. Your SENTRY_DSN is correct in .env")
    print("  2. SENTRY_ENABLED=true in .env")
    print("  3. Your internet connection is working")
    print("=" * 60)


if __name__ == "__main__":
    test_sentry_integration()
