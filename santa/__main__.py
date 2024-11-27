import sys

from .config import parse_args, load_config, get_organizers
from .pick import pick_santas
from .email import compile_emails, send_emails


def main() -> None:
    file_path, dry_run = parse_args(sys.argv[1:])
    cfg = load_config(file_path=file_path)
    organizers = get_organizers(participants=cfg.participants)
    picks = pick_santas(participants=cfg.participants)
    emails = compile_emails(
        picks=picks,
        organizers=organizers,
        sender=cfg.sender,
        email_template=cfg.email_template,
    )
    send_emails(emails=emails, dry_run=dry_run)


if __name__ == "__main__":
    main()
