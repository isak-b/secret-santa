import pytest
from unittest.mock import patch

from santa.pick import pick_santas
from santa.config import Participant


class TestPickSantas:
    participants = [
        Participant(name="Alice", email="alice@example.com"),
        Participant(name="Bob", email="bob@example.com"),
        Participant(name="Charlie", email="charlie@example.com"),
    ]

    def test_picks_len(self):
        # Ensure the number of picks matches the number of participants
        picks = pick_santas(self.participants)
        assert len(picks) == len(self.participants)

    def test_no_self_pairing(self):
        # Ensure no one is their own Secret Santa
        picks = pick_santas(self.participants)
        for pick in picks:
            assert pick.giver != pick.receiver

    def test_all_participants_are_givers_and_receivers(self):
        # Ensure every participant is a giver and a receiver once
        picks = pick_santas(self.participants)
        participant_names = {participant.name for participant in self.participants}
        giver_names = {pick.giver.name for pick in picks}
        receiver_names = {pick.receiver.name for pick in picks}
        assert set(giver_names) == set(participant_names)
        assert set(receiver_names) == set(participant_names)

    def test_too_few_participants(self):
        # Ensure ValueError is raised for fewer than 2 participants
        with pytest.raises(ValueError):
            pick_santas([self.participants[0]])  # Only one participant

    @patch("random.sample")
    def test_shuffling_logic(self, mock_sample):
        # Ensure `random.sample` is called correctly
        mock_sample.return_value = self.participants[::-1]  # Reverse order
        picks = pick_santas(self.participants)
        mock_sample.assert_called_once_with(self.participants, len(self.participants))
        picks[0].giver == self.participants[-1]
        picks[0].receiver == self.participants[-2]
