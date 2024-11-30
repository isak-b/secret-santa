import os
import argparse
import yaml
import dotenv

from pydantic import BaseModel, EmailStr
from typing import Optional, get_args

dotenv.load_dotenv(override=True)
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


class MissingConfigKeyError(Exception): ...


class Participant(BaseModel):
    name: str
    email: EmailStr
    organizer: Optional[bool] = False


class EmailTemplate(BaseModel):
    subject: str
    body: str


class Config(BaseModel):
    smtp_token: str | None = None
    sender_email: EmailStr
    email_template: EmailTemplate
    participants: list[Participant]


def parse_args(args: list[str]) -> tuple[str, bool]:
    parser = argparse.ArgumentParser(description="config file_path with optional --dry-run mode")
    parser.add_argument(
        "file_path",
        nargs="?",
        default=DEFAULT_PATH,
        help="path to the config.yaml file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="dry-run mode prints the emails instead of sending them",
    )
    file_path, dry_run = parser.parse_args(args).file_path, parser.parse_args(args).dry_run
    print(f"Arguments:\n- {file_path=}\n- {dry_run=}")
    return file_path, dry_run


def load_config(file_path: str) -> Config:
    """Load config values from the environment and config file"""

    # Add values from environment
    data = {
        "smtp_token": os.environ.get("SMTP_TOKEN"),
        "sender_email": os.environ.get("SENDER_EMAIL"),
    }
    env_keys = list(data)

    # Add values from config file
    with open(file_path, "r") as file:
        data.update(**yaml.safe_load(file))

    # Check for missing values
    for key in Config.model_fields.keys():
        if data[key] is None and type(None) not in get_args(Config.model_fields[key].annotation):
            error_msg = f"Missing config key: '{key}'. "
            if key in env_keys:
                error_msg += f"Export it with: `export {str(key).upper()}=<your {key}>`"
            else:
                error_msg += f"Add it to {file_path}: {key}: <your {key}>"
            raise MissingConfigKeyError(error_msg)

    return Config(**data)


def get_organizers(participants: list[Participant]) -> list[Participant]:
    return ", ".join(sorted([p.name for p in participants if p.organizer]))
