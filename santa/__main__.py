import sys

from .config import parse_args, load_config, get_organizers
from .pick import pick_santas
from .email import compile_emails, handle_emails


def main() -> None:
    file_path, dry_run = parse_args(sys.argv[1:])
    cfg = load_config(file_path=file_path)
    organizers = get_organizers(participants=cfg.participants)
    picks = pick_santas(participants=cfg.participants, seed=cfg.seed)
    emails = compile_emails(
        picks=picks,
        organizers=organizers,
        sender_email=cfg.sender_email,
        email_template=cfg.email_template,
    )
    handle_emails(emails=emails, smtp_token=cfg.smtp_token, dry_run=dry_run)


if __name__ == "__main__":
    main()
