import pytest
from unittest import TestCase
from unittest.mock import patch, MagicMock

from santa.config import Participant
from santa.pick import Pick
from santa.email import (
    Email,
    action_send,
    action_send_all,
    action_print,
    action_quit,
    handle_emails,
    compile_emails,
    EmailTemplate,
)


@pytest.fixture
def email():
    return Email(
        sender_email="sender@example.com",
        giver_email="giver@example.com",
        subject="Mock subject",
        body="Mock body",
    )


class TestActions:
    @patch("santa.email.SMTP")
    @patch("builtins.input")
    def test_action_send(self, mock_input, MockSMTP, email):
        mock_smtp_instance = MagicMock()
        MockSMTP.return_value = mock_smtp_instance
        mock_input.return_value = ""

        # Run test
        encoded_msg = 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nFrom: sender@example.com\nTo: giver@example.com\nSubject: Mock subject\n\nTW9jayBib2R5\n'
        action_send(email, "mock_smtp_token")
        MockSMTP.assert_called_once_with("smtp.gmail.com", port=587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(user="sender@example.com", password="mock_smtp_token")
        mock_smtp_instance.sendmail.assert_called_once_with(
            from_addr="sender@example.com",
            to_addrs="giver@example.com",
            msg=encoded_msg,
        )

    @patch("santa.email.action_send")
    @patch("builtins.input")
    def test_action_send_all(self, mock_input, mock_action_send, email):
        emails = [email, email]
        mock_input.return_value = ""

        # Run test
        action_send_all(emails, "mock_smtp_token")
        assert mock_action_send.call_count == 2
        for call in mock_action_send.call_args_list:
            assert len(call.args) + len(call.kwargs) == 2
            email_obj, smtp_token = list(call.args) + list(call.kwargs.values())
            assert email_obj == email
            assert smtp_token == "mock_smtp_token"

    @patch("builtins.print")
    @patch("builtins.input")
    def test_action_print(self, mock_input, mock_print, email):
        mock_input.return_value = ""

        # Run test
        action_print(email)
        mock_print.assert_called_once()

    @patch("builtins.exit")
    def test_action_quit(self, mock_exit):
        # Run test
        action_quit()
        mock_exit.assert_called_once_with(0)


class TestHandleEmails(TestCase):
    def setUp(self):
        self.patcher_send = patch("santa.email.action_send")
        self.patcher_send_all = patch("santa.email.action_send_all")
        self.patcher_print = patch("santa.email.action_print")
        self.patcher_quit = patch("santa.email.action_quit")

        self.mock_send = self.patcher_send.start()
        self.mock_send_all = self.patcher_send_all.start()
        self.mock_print = self.patcher_print.start()
        self.mock_quit = self.patcher_quit.start()

        self.actions_map = {
            "send": self.mock_send,
            "send all": self.mock_send_all,
            "print": self.mock_print,
            "quit": self.mock_quit,
        }

        self.email = Email(
            sender_email="sender@example.com",
            giver_email="giver@example.com",
            subject="Mock subject",
            body="Mock body",
        )

    def tearDown(self):
        patch.stopall()

    def _check_action_call(self, action, kwargs):
        self.actions_map[action].assert_called_once_with(**kwargs)

    def _check_action_call_counts(self, expected_calls):
        for expected_action, expected_count in expected_calls.items():
            actual_count = self.actions_map[expected_action].call_count
            self.assertEqual(
                actual_count,
                expected_count,
                f"Expected {expected_action} to be called {expected_count} times, but it was called {actual_count} times.",
            )

    @patch("santa.email.select_action")
    def test_handle_emails_send(self, mock_select_action):
        emails = [self.email]
        mock_select_action.side_effect = ["send"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_kwargs = {"email": emails[0], "smtp_token": "mock_smtp_token"}
        self._check_action_call(action="send", kwargs=expected_kwargs)

        expected_calls = {"send": 1, "send all": 0, "print": 0, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    def test_handle_emails_send_all(self, mock_select_action):
        emails = [self.email, self.email]
        mock_select_action.side_effect = ["send all"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_kwargs = {"emails": emails, "smtp_token": "mock_smtp_token"}
        self._check_action_call(action="send all", kwargs=expected_kwargs)

        expected_calls = {"send": 0, "send all": 1, "print": 0, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    def test_handle_emails_print(self, mock_select_action):
        emails = [self.email]
        mock_select_action.side_effect = ["print", "skip"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_kwargs = {"email": emails[0]}
        self._check_action_call(action="print", kwargs=expected_kwargs)

        expected_calls = {"send": 0, "send all": 0, "print": 1, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    def test_handle_emails_print(self, mock_select_action):
        emails = [self.email]
        mock_select_action.side_effect = ["print", "skip"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_kwargs = {"email": emails[0]}
        self._check_action_call(action="print", kwargs=expected_kwargs)

        expected_calls = {"send": 0, "send all": 0, "print": 1, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    def test_handle_emails_skip(self, mock_select_action):
        emails = [self.email]
        mock_select_action.side_effect = ["skip"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_kwargs = {}
        self._check_action_call(action="quit", kwargs=expected_kwargs)

        expected_calls = {"send": 0, "send all": 0, "print": 0, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    def test_handle_emails_quit(self, mock_select_action):
        emails = [self.email]
        mock_select_action.side_effect = ["quit"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_kwargs = {}
        self._check_action_call(action="quit", kwargs=expected_kwargs)

        expected_calls = {"send": 0, "send all": 0, "print": 0, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    def test_handle_emails_multiple(self, mock_select_action):
        emails = [self.email, self.email, self.email, self.email]
        mock_select_action.side_effect = ["send", "print", "send", "send all", "quit"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_calls = {"send": 2, "send all": 1, "print": 1, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    def test_handle_emails_with_no_emails(self, mock_select_action):
        emails = []
        mock_select_action.side_effect = ["send", "print", "send", "send all", "quit"]
        handle_emails(emails, smtp_token="mock_smtp_token")

        expected_calls = {"send": 0, "send all": 0, "print": 0, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)

    @patch("santa.email.select_action")
    @patch("builtins.input")
    def test_handle_emails_with_no_emails(self, mock_input, mock_select_action):
        emails = [self.email]
        mock_input.return_value = "foo bar"
        mock_select_action.side_effect = ["send"]
        handle_emails(emails)

        expected_kwargs = {"email": emails[0], "smtp_token": "foo bar"}
        self._check_action_call(action="send", kwargs=expected_kwargs)

        expected_calls = {"send": 1, "send all": 0, "print": 0, "quit": 1}
        self._check_action_call_counts(expected_calls=expected_calls)


class TestCompileEmails:
    def test_compile_emails(self):
        picks = [
            Pick(
                giver=Participant(email="participant1@example.com", name="Participant 1"),
                receiver=Participant(email="participant2@example.com", name="Participant 2"),
            ),
            Pick(
                giver=Participant(email="participant2@example.com", name="Participant 2"),
                receiver=Participant(email="participant1@example.com", name="Participant 1"),
            ),
        ]
        organizers = "Mock organizer"
        sender_email = "organizer@example.com"
        body_template = "Mock: {giver}-{receiver}-{organizers}"
        email_template = EmailTemplate(subject="Mock subject", body=body_template)
        emails = compile_emails(
            picks=picks, organizers=organizers, sender_email=sender_email, email_template=email_template
        )

        # Run test
        expected_bodies = [
            f"Mock: {picks[i].giver.name}-{picks[i].receiver.name}-{organizers}" for i in range(len(picks))
        ]
        assert len(emails) == len(picks) == len(expected_bodies)
        for email, expected_body in zip(emails, expected_bodies):
            assert email.sender_email == sender_email
            assert email.subject == email_template.subject
            assert email.body == expected_body
