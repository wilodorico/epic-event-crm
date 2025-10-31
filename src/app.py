from collaborators.infrastructure.cli import cli
from collaborators.infrastructure.sentry_config import init_sentry

if __name__ == "__main__":
    # Initialize Sentry for error tracking and monitoring
    init_sentry()

    cli.cli()
