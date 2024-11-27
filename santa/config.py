import os
import argparse
import yaml
import dotenv

from pydantic import BaseModel, EmailStr
from typing import Optional

dotenv.load_dotenv()
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


class Participant(BaseModel):
    name: str
    email: EmailStr
    organizer: Optional[bool] = False


class EmailTemplate(BaseModel):
    subject: str
    body: str


class Config(BaseModel):
    participants: list[Participant]
    email_template: EmailTemplate
    sender: EmailStr = os.environ["SENDER_EMAIL"]


def parse_args(args: list[str]) -> tuple[str, bool]:
    parser = argparse.ArgumentParser(description="Process file path with optional dry-run mode.")
    parser.add_argument(
        "file_path",
        nargs="?",
        default=DEFAULT_PATH,
        help="The path to the config.yaml file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="dry-run mode prints the santa e-mails instead of sending them.",
    )
    file_path, dry_run = parser.parse_args(args).file_path, parser.parse_args(args).dry_run
    print(f"Arguments:\n- {file_path=}\n- {dry_run=}")
    return file_path, dry_run


def load_config(file_path: str) -> Config:
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return Config(**data)


def get_organizers(participants: list[Participant]) -> list[Participant]:
    return ", ".join(sorted([p.name for p in participants if p.organizer]))
