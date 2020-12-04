"""
Triggers a Workflow from another repository using "repository_dispatch" event
"""
import logging
import os
import sys

import requests
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, rich_tracebacks=True)],
)

install()
logger = logging.getLogger("main")


def get_endpoint(repo):
    return f"https://api.github.com/repos/{repo}/dispatches"


def start():
    pat = os.environ["INPUT_GITHUB_PAT"]
    repository = os.environ["INPUT_REPOSITORY"]
    event = os.environ["INPUT_EVENT"]

    headers = {
        "Accept": "application/vnd.github.everest-preview+json",
        "Authorization": f"token {pat}",
    }
    client_payload = {
        k.removeprefix("PAYLOAD_"): v
        for k, v in os.environ.items()
        if k.startswith("PAYLOAD_")
    }
    body = {
        "event_type": event,
        "client_payload": client_payload,
    }
    endpoint = get_endpoint(repository)
    response = requests.post(endpoint, json=body, headers=headers)
    if not response.ok:
        logger.error(response.status_code)
        try:
            logger.error(response.json()["message"])
        except (ValueError, IndexError):
            logger.error(response.text)
        sys.exit(1)
    logger.info(f"Event {event} successfully dispatched")


if __name__ == "__main__":
    start()
