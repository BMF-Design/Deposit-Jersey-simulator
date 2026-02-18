from enum import Enum, auto
from dataclasses import dataclass


class Role(Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"


class GameState(Enum):
    START = auto()
    AGREEMENT_SIGNED = auto()
    DEPOSIT_PAID = auto()
    DEPOSIT_PROTECTED = auto()
    MID_TENANCY = auto()
    END_NOTICE_GIVEN = auto()
    CHECKOUT_DONE = auto()
    DEPOSIT_PROPOSED = auto()
    ADR_DISPUTE = auto()
    GAME_OVER = auto()


@dataclass
class PlayerStats:
    compliance: int = 0
    trust: int = 0
    evidence: int = 0
    legal_risk: int = 0