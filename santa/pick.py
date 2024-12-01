import random
from pydantic import BaseModel, EmailStr
from typing import Optional


class Participant(BaseModel):
    name: str
    email: EmailStr
    organizer: Optional[bool] = False


class Pick(BaseModel):
    giver: Participant
    receiver: Participant
    seed: Optional[int] = None


def pick_santas(participants: list[Participant], seed: Optional[int] = None) -> list[Pick]:
    if len(participants) < 2:
        raise ValueError("At least two participants are required for Secret Santa.")

    # Set random state (for reproducibility)
    if seed is None:
        seed = random.randrange(1000, 9999)
    random.seed(seed)

    print("\nPicks:")
    print(f"- {len(participants)=}")
    print(f"- {seed=}")
    print(f"- NOTE: Set config.seed={seed} to reproduce these picks")

    shuffled_participants = random.sample(participants, len(participants))
    picks = []
    for i in range(len(shuffled_participants)):
        giver = shuffled_participants[i]
        receiver = shuffled_participants[(i + 1) % len(shuffled_participants)]
        picks.append(Pick(giver=giver, receiver=receiver, seed=seed))
    return picks
