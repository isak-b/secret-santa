from smtplib import SMTP

from email.mime.text import MIMEText
from typing import Literal
from pydantic import BaseModel, EmailStr
from simple_term_menu import TerminalMenu

from .pick import Pick

DELIM = "-" * 50
ACTION = Literal["send", "print", "skip", "send all", "quit"]


class EmailTemplate(BaseModel):
    subject: str
    body: str


def action_send(email, smtp_token: str):
    print(f"Sending email to {email.giver_email}\n")
    msg = MIMEText(email.body, "plain", "utf-8")
    msg["From"] = email.sender_email
    msg["To"] = email.giver_email
    msg["Subject"] = email.subject

    con = SMTP("smtp.gmail.com", port=587)
    con.starttls()
    con.login(user=email.sender_email, password=smtp_token)
    con.sendmail(from_addr=email.sender_email, to_addrs=email.giver_email, msg=msg.as_string())
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


def select_action(dry_run: bool = False) -> ACTION:
    all_actions = ["send", "print", "skip", "send all", "quit"]
    exclude = ["send", "send all"] if dry_run else []
    actions = [action for action in all_actions if action not in exclude]
    terminal_menu = TerminalMenu(actions, title="Select action:")
    terminal_menu.show()
    action = terminal_menu.chosen_menu_entry
    return action


def handle_emails(emails: list[Email], smtp_token: str = None, dry_run: bool = False, i: int = 0) -> None:
    if i >= len(emails):
        action_quit()
        return

    print(f"\n{DELIM}\nEMAIL {i+1} / {len(emails)}\n")
    print(f"FROM: {emails[i].sender_email}")
    print(f"TO: {emails[i].giver_email}\n")

    action = select_action(dry_run=dry_run)

    # Check SMTP token
    if action in ["send", "send all"] and smtp_token is None:
        smtp_token = input("Enter SMTP token: ").strip()

    # Execute action
    if action == "send":
        action_send(email=emails[i], smtp_token=smtp_token)
        handle_emails(emails=emails, smtp_token=smtp_token, dry_run=dry_run, i=i + 1)
    elif action == "send all":
        action_send_all(emails=emails[i:], smtp_token=smtp_token)
        action_quit()
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
