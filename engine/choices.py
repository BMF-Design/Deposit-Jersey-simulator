from dataclasses import dataclass
from typing import Dict, List, Tuple

from engine.states import Role, GameState


@dataclass
class Choice:
    id: str
    text: str
    next_state: GameState
    compliance_delta: int = 0
    trust_delta: int = 0
    evidence_delta: int = 0
    legal_risk_delta: int = 0
    law_reference: str = ""
    explanation: str = ""


# Short scene descriptions for each (role, state)
SCENES: Dict[Tuple[Role, GameState], str] = {
    (Role.TENANT, GameState.START): (
        "You are a tenant about to sign a new tenancy agreement. "
        "The landlord is asking for a deposit equal to one month's rent."
    ),
    (Role.TENANT, GameState.AGREEMENT_SIGNED): (
        "You have signed the tenancy agreement and are preparing to pay the deposit."
    ),
    (Role.TENANT, GameState.DEPOSIT_PAID): (
        "You have paid the deposit to the landlord. The 30-day clock for deposit protection is now ticking."
    ),

    (Role.LANDLORD, GameState.START): (
        "You are a landlord preparing a new tenancy. You plan to take a deposit from the tenant."
    ),
    (Role.LANDLORD, GameState.AGREEMENT_SIGNED): (
        "Your tenant has signed the tenancy agreement and is about to pay the deposit."
    ),
    (Role.LANDLORD, GameState.DEPOSIT_PAID): (
        "You have received the tenant's deposit. You now have 30 days to protect it in the approved scheme."
    ),
}


# Choices for each (role, state)
CHOICES: Dict[Tuple[Role, GameState], List[Choice]] = {
    # ---------- Tenant path ----------
    (Role.TENANT, GameState.START): [
        Choice(
            id="T1_READ",
            text="Read the tenancy agreement carefully and ask questions before signing.",
            next_state=GameState.AGREEMENT_SIGNED,
            compliance_delta=1,
            trust_delta=1,
            explanation="Good choice. Understanding the agreement helps you know how your deposit can be used."
        ),
        Choice(
            id="T1_SKIP",
            text="Sign quickly without really reading the agreement.",
            next_state=GameState.AGREEMENT_SIGNED,
            compliance_delta=0,
            trust_delta=-1,
            explanation="Risky choice. You may miss important clauses about the deposit and your obligations."
        ),
    ],

    (Role.TENANT, GameState.AGREEMENT_SIGNED): [
        Choice(
            id="T2_TRACEABLE",
            text="Pay the deposit by bank transfer and keep the payment confirmation.",
            next_state=GameState.DEPOSIT_PAID,
            compliance_delta=1,
            evidence_delta=1,
            explanation="Excellent. A traceable payment and receipt make it easier to prove you paid the deposit."
        ),
        Choice(
            id="T2_CASH",
            text="Pay the deposit in cash without getting a receipt.",
            next_state=GameState.DEPOSIT_PAID,
            evidence_delta=-1,
            explanation="This makes it harder to prove you paid if there is a dispute later."
        ),
    ],

    (Role.TENANT, GameState.DEPOSIT_PAID): [
        Choice(
            id="T3_CHECK_PROTECTION",
            text="Make a note to check within 30 days that your deposit is protected.",
            next_state=GameState.MID_TENANCY,
            compliance_delta=1,
            evidence_delta=1,
            explanation="Good habit. Tenants should check they receive a Deposit Protection Certificate or scheme confirmation."
        ),
        Choice(
            id="T3_FORGET",
            text="Assume everything is fine and never check whether the deposit is protected.",
            next_state=GameState.MID_TENANCY,
            compliance_delta=-1,
            explanation="If the landlord does not protect the deposit, you might only discover it when there is a problem."
        ),
    ],

    # ---------- Landlord path ----------
    (Role.LANDLORD, GameState.START): [
        Choice(
            id="L1_FAIR_DEPOSIT",
            text="Set the deposit at one month's rent and put everything in a written agreement.",
            next_state=GameState.AGREEMENT_SIGNED,
            compliance_delta=1,
            trust_delta=1,
            explanation="Good practice. A clear written agreement and reasonable deposit support a fair tenancy."
        ),
        Choice(
            id="L1_HIGH_DEPOSIT",
            text="Demand a very high deposit and don't bother with a detailed agreement.",
            next_state=GameState.AGREEMENT_SIGNED,
            trust_delta=-2,
            legal_risk_delta=1,
            explanation="This may scare off tenants and could increase the risk of disputes about what the deposit covers."
        ),
    ],

    (Role.LANDLORD, GameState.AGREEMENT_SIGNED): [
        Choice(
            id="L2_RECEIPT",
            text="Give the tenant a clear receipt when you receive the deposit.",
            next_state=GameState.DEPOSIT_PAID,
            compliance_delta=1,
            trust_delta=1,
            explanation="Transparent record-keeping builds trust and helps if there are later questions about the deposit."
        ),
        Choice(
            id="L2_NORECEIPT",
            text="Take the money but don't give any written confirmation.",
            next_state=GameState.DEPOSIT_PAID,
            trust_delta=-1,
            legal_risk_delta=1,
            explanation="Poor practice. Lack of documentation makes disputes more likely and harder to resolve."
        ),
    ],

    (Role.LANDLORD, GameState.DEPOSIT_PAID): [
        Choice(
            id="L3_PROTECT",
            text="Protect the deposit in the approved scheme within 30 days.",
            next_state=GameState.MID_TENANCY,
            compliance_delta=2,
            trust_delta=1,
            legal_risk_delta=-1,
            explanation="Correct. Protecting the deposit on time reduces your legal risk and reassures the tenant."
        ),
        Choice(
            id="L3_DELAY",
            text="Wait and see, maybe protect it later or not at all.",
            next_state=GameState.MID_TENANCY,
            compliance_delta=-2,
            legal_risk_delta=2,
            explanation="Dangerous. Failing to protect the deposit on time can lead to penalties and disputes."
        ),
    ],
}