import pytest
from unittest.mock import patch, MagicMock

from santa.email import Email, action_send, action_send_all, action_print, action_quit, handle_emails


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
        action_send(email, "mock_smtp_token")
        MockSMTP.assert_called_once_with("smtp.gmail.com", port=587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with("sender@example.com", "mock_smtp_token")
        mock_smtp_instance.sendmail.assert_called_once_with(
            "sender@example.com", "giver@example.com", f"Subject: {email.subject}\n\n{email.body}"
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


class TestHandleEmails:
    @patch("santa.email.TerminalMenu")
    @patch("santa.email.action_send")
    @patch("santa.email.action_send_all")
    @patch("santa.email.action_print")
    @patch("santa.email.action_quit")
    @patch("builtins.input", return_value="mock_smtp_token")
    def test_handle_emails_send(
        self,
        mock_input,
        mock_action_quit,
        mock_action_print,
        mock_action_send_all,
        mock_action_send,
        mock_terminal_menu,
        email,
    ):
        emails = [email]
        mock_input.return_value = ""
        mock_terminal_menu.return_value.chosen_menu_entry = "send"
        mock_terminal_menu.return_value.show = MagicMock()

        # Run test
        handle_emails(emails, smtp_token="mock_smtp_token")
        mock_action_send.assert_called_once_with(email=emails[0], smtp_token="mock_smtp_token")
        mock_action_send_all.assert_not_called()
        mock_action_print.assert_not_called()
        mock_action_quit.assert_called_once()

    @patch("santa.email.TerminalMenu")
    @patch("santa.email.action_send")
    @patch("santa.email.action_send_all")
    @patch("santa.email.action_print")
    @patch("santa.email.action_quit")
    @patch("builtins.input", return_value="mock_smtp_token")
    def test_handle_emails_send_all(
        self,
        mock_input,
        mock_action_quit,
        mock_action_print,
        mock_action_send_all,
        mock_action_send,
        mock_terminal_menu,
        email,
    ):
        emails = [email]
        mock_input.return_value = ""
        mock_terminal_menu.return_value.chosen_menu_entry = "send all"
        mock_terminal_menu.return_value.show = MagicMock()

        # Run test
        handle_emails(emails, smtp_token="mock_smtp_token")
        mock_action_send.assert_not_called()
        mock_action_send_all.assert_called_once_with(emails=emails, smtp_token="mock_smtp_token")
        mock_action_print.assert_not_called()
        mock_action_quit.assert_not_called()

    @patch("santa.email.TerminalMenu")
    @patch("santa.email.action_send")
    @patch("santa.email.action_send_all")
    @patch("santa.email.action_print")
    @patch("santa.email.action_quit")
    @patch("builtins.input", return_value="mock_smtp_token")
    def test_handle_emails_skip(
        self,
        mock_input,
        mock_action_quit,
        mock_action_print,
        mock_action_send_all,
        mock_action_send,
        mock_terminal_menu,
        email,
    ):
        emails = [email]
        mock_input.return_value = ""
        mock_terminal_menu.return_value.chosen_menu_entry = "skip"
        mock_terminal_menu.show = MagicMock()

        # Run test
        handle_emails(emails, smtp_token="mock_smtp_token")
        mock_action_send.assert_not_called()
        mock_action_send_all.assert_not_called()
        mock_action_print.assert_not_called()
        mock_action_quit.assert_called_once()

    # TODO: Write test for print
    # @patch("santa.email.TerminalMenu")
    # @patch("santa.email.action_send")
    # @patch("santa.email.action_send_all")
    # @patch("santa.email.action_print")
    # @patch("santa.email.action_quit")
    # @patch("builtins.input", return_value="mock_smtp_token")
    # def test_handle_emails_print(
    #     self,
    #     mock_input,
    #     mock_action_quit,
    #     mock_action_print,
    #     mock_action_send_all,
    #     mock_action_send,
    #     mock_terminal_menu,
    #     email,
    # ):
    #     emails = [email]
    #     mock_input.return_value = ""
