import random
from pydantic import BaseModel

from .config import Participant


class Pick(BaseModel):
    giver: Participant
    receiver: Participant


def pick_santas(participants: list[Participant]) -> list[Pick]:
    if len(participants) < 2:
        raise ValueError("At least two participants are required for Secret Santa.")

    shuffled_participants = random.sample(participants, len(participants))
    picks = []
    for i in range(len(shuffled_participants)):
        giver = shuffled_participants[i]
        receiver = shuffled_participants[(i + 1) % len(shuffled_participants)]
        picks.append(Pick(giver=giver, receiver=receiver))
    return picks
