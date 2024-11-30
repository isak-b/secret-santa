from smtplib import SMTP

from pydantic import BaseModel, EmailStr
from simple_term_menu import TerminalMenu

from .config import EmailTemplate
from .pick import Pick

DELIM = "-" * 50


def action_send(email, smtp_token: str):
    print(f"Sending email to {email.giver_email}\n")
    con = SMTP("smtp.gmail.com", port=587)
    con.starttls()
    con.login(email.sender_email, smtp_token)
    con.sendmail(email.sender_email, email.giver_email, f"Subject: {email.subject}\n\n{email.body}")
    print("Email sent!\n")
    input("Press enter to continue...")


def action_send_all(emails, smtp_token: str):
    print("\nSending all emails...\n")
    for email in emails:
        action_send(email=email, smtp_token=smtp_token)


def action_print(email):
    print(f"{DELIM}\n{email.subject}\n{email.body}")
    input("Press enter to continue...")


def action_quit():
    print("Quitting program...")
    exit(0)


class Email(BaseModel):
    sender_email: EmailStr
    giver_email: EmailStr
    subject: str
    body: str


def compile_emails(
    picks: list[Pick],
    organizers: str,
    sender_email: EmailStr,
    email_template: EmailTemplate,
) -> list[Email]:
    emails = []
    for pick in picks:
        email = Email(
            sender_email=sender_email,
            giver_email=pick.giver.email,
            subject=email_template.subject,
            body=email_template.body.format(
                giver=pick.giver.name,
                receiver=pick.receiver.name,
                organizers=organizers,
            ),
        )
        emails.append(email)
    return emails


def handle_emails(emails: list[Email], smtp_token: str = None, dry_run: bool = False, i: int = 0) -> None:
    if i >= len(emails):
        action_quit()
        return

    print(f"\n{DELIM}\nEMAIL {i+1} / {len(emails)}\n")
    print(f"FROM: {emails[i].sender_email}")
    print(f"TO: {emails[i].giver_email}\n")

    # Select action
    actions = ["send", "print", "skip", "send all", "quit"]
    actions = [action for action in actions if dry_run is False or action not in ["send", "send all"]]
    terminal_menu = TerminalMenu(actions, title="Select action:")
    terminal_menu.show()
    action = terminal_menu.chosen_menu_entry

    # Check SMTP token
    if action in ["send", "send all"] and smtp_token is None:
        smtp_token = input("Enter SMTP token: ").strip()

    # Execute action
    if action == "send":
        action_send(email=emails[i], smtp_token=smtp_token)
        handle_emails(emails=emails, smtp_token=smtp_token, dry_run=dry_run, i=i + 1)
    elif action == "send all":
        action_send_all(emails=emails[i:], smtp_token=smtp_token)
    elif action == "print":
        # NOTE: print does not increase i
        action_print(email=emails[i])
        handle_emails(emails=emails, smtp_token=smtp_token, dry_run=dry_run, i=i)
    elif action == "skip":
        handle_emails(emails=emails, smtp_token=smtp_token, dry_run=dry_run, i=i + 1)
    elif action in ["quit", "q"]:
        action_quit()
    else:
        handle_emails(emails=emails, smtp_token=smtp_token, dry_run=dry_run, i=i)
