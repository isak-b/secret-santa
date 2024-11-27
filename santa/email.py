from pydantic import BaseModel, EmailStr

from .config import EmailTemplate
from .pick import Pick


class Email(BaseModel):
    sender: EmailStr
    to: EmailStr
    subject: str
    body: str


def compile_emails(
    picks: list[Pick],
    organizers: str,
    sender: EmailStr,
    email_template: EmailTemplate,
) -> list[Email]:
    emails = []
    for pick in picks:
        email = Email(
            sender=sender,
            to=pick.receiver.email,
            subject=email_template.subject,
            body=email_template.body.format(
                giver=pick.giver.name,
                receiver=pick.receiver.name,
                organizers=organizers,
            ),
        )
        emails.append(email)
    return emails


def send_emails(emails: list[Email], dry_run: bool = False) -> None:
    delim = "-" * 30
    for i, email in enumerate(emails):
        msg = f"{delim}\nEMAIL {i + 1} / {len(emails)} ({dry_run=}):\n{delim}\n"
        msg += f"from: {email.sender}\nto: {email.to}\n"
        if dry_run is True:
            msg += f"\nsubject: {email.subject}\n{email.body}"
            msg += ">>> email NOT sent"
        else:
            # TODO: Send email using SMTP
            msg += ">>> email sent"
        print(msg)
