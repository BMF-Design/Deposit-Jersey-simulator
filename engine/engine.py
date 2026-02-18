from typing import List

from engine.states import Role, GameState, PlayerStats
from engine.choices import CHOICES, SCENES, Choice


class GameEngine:
    def __init__(self, role: Role):
        self.role = role
        self.state = GameState.START
        self.stats = PlayerStats()

    def get_scene_text(self) -> str:
        return SCENES.get(
            (self.role, self.state),
            "No scene defined for this state yet.",
        )

    def get_choices(self) -> List[Choice]:
        return CHOICES.get((self.role, self.state), [])

    def apply_choice(self, choice_index: int) -> str:
        choices = self.get_choices()
        if not choices:
            return "There are no choices available from this state."

        if choice_index < 0 or choice_index >= len(choices):
            return "Invalid choice number."

        choice = choices[choice_index]

        # Update stats
        self.stats.compliance += choice.compliance_delta
        self.stats.trust += choice.trust_delta
        self.stats.evidence += choice.evidence_delta
        self.stats.legal_risk += choice.legal_risk_delta

        # Move to next state
        self.state = choice.next_state

        return choice.explanation

    def is_game_over(self) -> bool:
        # Later you can mark some states as final
        return self.state == GameState.GAME_OVER