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
      (Role.TENANT, GameState.MID_TENANCY): [
        Choice(
            id="T4_REPORT_ISSUE",
            text="Report a maintenance issue to the landlord in writing.",
            next_state=GameState.END_NOTICE_GIVEN,
            compliance_delta=1,
            evidence_delta=1,
            explanation="Written communication creates evidence if disputes arise."
        ),
        Choice(
            id="T4_VERBAL",
            text="Mention a problem verbally when you see the landlord.",
            next_state=GameState.END_NOTICE_GIVEN,
            trust_delta=1,
            explanation="Verbal communication may solve issues but leaves no record."
        ),
        Choice(
            id="T4_IGNORE",
            text="Ignore minor problems in the property.",
            next_state=GameState.END_NOTICE_GIVEN,
            trust_delta=-1,
            explanation="Unreported problems can worsen and lead to disagreements later."
        ),
    ],
    (Role.TENANT, GameState.END_NOTICE_GIVEN): [
    Choice(
        id="T5_PROPER_NOTICE",
        text="Give proper written notice according to the tenancy agreement.",
        next_state=GameState.CHECKOUT_DONE,
        compliance_delta=1,
        evidence_delta=1,
        explanation="Good practice. Written notice avoids disputes later."
    ),
    Choice(
        id="T5_LAST_MINUTE",
        text="Leave suddenly without formal notice.",
        next_state=GameState.CHECKOUT_DONE,
        trust_delta=-1,
        explanation="Poor communication may lead to deductions or disputes."
    ),
],
    (Role.TENANT, GameState.CHECKOUT_DONE): [
    Choice(
        id="T6_PHOTOS",
        text="Take photos of the property condition before leaving.",
        next_state=GameState.DEPOSIT_PROPOSED,
        evidence_delta=2,
        explanation="Photos provide strong evidence in case of a dispute."
    ),
    Choice(
        id="T6_INSPECTION",
        text="Walk through the property with the landlord.",
        next_state=GameState.DEPOSIT_PROPOSED,
        trust_delta=1,
        explanation="Joint inspection may reduce disputes."
    ),
    Choice(
        id="T6_NOTHING",
        text="Leave without documenting the condition.",
        next_state=GameState.DEPOSIT_PROPOSED,
        evidence_delta=-1,
        explanation="Lack of documentation weakens your position."
    ),
],
    (Role.TENANT, GameState.DEPOSIT_PROPOSED): [
    Choice(
        id="T7_ACCEPT",
        text="Accept the landlord's proposed deductions.",
        next_state=GameState.GAME_OVER,
        explanation="The tenancy dispute ends."
    ),
    Choice(
        id="T7_NEGOTIATE",
        text="Discuss the deductions with the landlord.",
        next_state=GameState.ADR_DISPUTE,
        trust_delta=1,
        explanation="Communication may resolve the dispute."
    ),
    Choice(
        id="T7_DISPUTE",
        text="Submit a dispute to the deposit scheme.",
        next_state=GameState.ADR_DISPUTE,
        evidence_delta=1,
        explanation="The dispute will go to ADR adjudication."
    ),
],
    (Role.TENANT, GameState.ADR_DISPUTE): [
    Choice(
        id="T8_STRONG_EVIDENCE",
        text="Submit strong documentation and evidence.",
        next_state=GameState.GAME_OVER,
        evidence_delta=2,
        explanation="Strong evidence improves your chances."
    ),
    Choice(
        id="T8_LIMITED",
        text="Submit limited documentation.",
        next_state=GameState.GAME_OVER,
        explanation="Outcome may be mixed."
    ),
    Choice(
        id="T8_NONE",
        text="Submit little evidence.",
        next_state=GameState.GAME_OVER,
        evidence_delta=-2,
        explanation="Weak documentation weakens your case."
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
        Choice(
            id="L1_POOR",
            text="Agree the tenancy informally without clear deposit terms.",
            next_state=GameState.AGREEMENT_SIGNED,
            trust_delta=-2,
            legal_risk_delta=1,
            explanation="Poor practice and increases legal risk."
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

    (Role.LANDLORD, GameState.MID_TENANCY): [
        Choice(
            id="L4_FIX_REPAIR",
            text="Respond quickly to repair requests and document the work.",
            next_state=GameState.END_NOTICE_GIVEN,
            compliance_delta=1,
            trust_delta=1,
            explanation="Responsible landlords keep records and address issues promptly."
        ),
        Choice(
            id="L4_IGNORE_REPAIR",
            text="Delay repairs and avoid documenting problems.",
            next_state=GameState.END_NOTICE_GIVEN,
            trust_delta=-2,
            legal_risk_delta=1,
            explanation="Ignoring maintenance can damage trust and increase disputes."
        ),
],

    (Role.LANDLORD, GameState.END_NOTICE_GIVEN): [
        Choice(
            id="L5_PLAN_CHECKOUT",
            text="Arrange a checkout inspection and review the inventory.",
            next_state=GameState.CHECKOUT_DONE,
            compliance_delta=1,
            evidence_delta=1,
            explanation="Good landlords compare the property to the inventory."
        ),
        Choice(
            id="L5_SKIP_CHECKOUT",
            text="Skip a proper checkout inspection.",
            next_state=GameState.CHECKOUT_DONE,
            evidence_delta=-1,
            explanation="Without inspection evidence it becomes harder to justify deductions."
        ),
],

    (Role.LANDLORD, GameState.CHECKOUT_DONE): [
        Choice(
            id="L6_FAIR_REVIEW",
            text="Review the property condition fairly against the inventory.",
            next_state=GameState.DEPOSIT_PROPOSED,
            compliance_delta=1,
            trust_delta=1,
            explanation="Fair comparison helps avoid disputes."
        ),
        Choice(
            id="L6_EXAGGERATE",
            text="Claim excessive damage to maximise deductions.",
            next_state=GameState.DEPOSIT_PROPOSED,
            trust_delta=-2,
            legal_risk_delta=2,
            explanation="Unfair deductions often lead to ADR disputes."
        ),
],

    (Role.LANDLORD, GameState.DEPOSIT_PROPOSED): [
        Choice(
            id="L7_REASONABLE",
            text="Propose reasonable deductions with evidence.",
            next_state=GameState.GAME_OVER,
            compliance_delta=1,
            explanation="Fair evidence-based deductions usually resolve quickly."
        ),
        Choice(
            id="L7_PUSH_LIMIT",
            text="Push large deductions hoping the tenant accepts.",
            next_state=GameState.ADR_DISPUTE,
            legal_risk_delta=1,
            explanation="Excessive claims often end up in ADR disputes."
        ),
],

    (Role.LANDLORD, GameState.ADR_DISPUTE): [
        Choice(
            id="L8_STRONG_CASE",
            text="Provide inventory, inspection records and receipts.",
            next_state=GameState.GAME_OVER,
            compliance_delta=1,
            evidence_delta=1,
            explanation="Detailed documentation strengthens your case."
        ),
        Choice(
            id="L8_WEAK_CASE",
            text="Submit limited documentation.",
            next_state=GameState.GAME_OVER,
            evidence_delta=-1,
            explanation="Weak evidence may result in losing the dispute."
        ),
],
}