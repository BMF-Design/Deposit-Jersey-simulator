from typing import List
import random

def clamp(value, min_v, max_v):
    return max(min_v, min(value, max_v))

from engine.states import Role, GameState, PlayerStats
from engine.scenes import SCENES
from engine.choices import CHOICES, Choice
from engine.property_system import PropertySystem
from engine.timeline import Timeline


class GameEngine:

    def __init__(self, role: Role):
        self.role = role
        self.state = GameState.START
        self.stats = PlayerStats()

        self.property = PropertySystem()
        self.timeline = Timeline()

        self.last_event_message = ""
        self.last_explanation = ""
        self.outcome = ""

    def get_current_node(self):
        return SCENES.get(
            (self.role, self.state),
            {
                "title": "Missing Scene",
                "text": "No scene defined for this state yet.",
                "choices": []
            }
        )

    def get_scene_text(self) -> str:
        return SCENES.get(
            (self.role, self.state),
            "No scene defined for this state yet.",
        )

    def get_weather(self) -> str:

        score = (
            self.stats.compliance
            + self.stats.trust
            + self.stats.evidence
            - self.stats.legal_risk
        )

        property_health = self.property.overall_health()

        # property condition affects weather
        if property_health < 50:
            score -= 2
        elif property_health > 85:
            score += 1
        if score >= 5:
            return "Sunny"
    
        elif score >= 1:
            return "Windy"
        else:
            return "Stormy"
    
    def get_weather_state(self) -> str:

        # No decisions made yet
        if (
            self.stats.compliance == 0
            and self.stats.trust == 0
            and self.stats.evidence == 0
            and self.stats.legal_risk == 0
        ):
            return "Pending"

        return self.get_weather()
    
    def evaluate_outcome(self):

        score = (
            self.stats.compliance
            + self.stats.trust
            + self.stats.evidence
        - self.stats.legal_risk
    )

        # Evidence is very important in ADR
        if self.stats.evidence >= 3 and score >= 3:
            self.outcome = "🏆 Strong evidence. The adjudicator rules largely in your favour."

        elif self.stats.evidence >= 1 and score >= 0:
            self.outcome = "⚖️ Mixed outcome. Some deductions are accepted."

        elif self.stats.evidence <= 0:
            self.outcome = "❗ Lack of evidence. The decision goes against you."
    
        else:
            self.outcome = "⚖️ Partial decision. Evidence was limited."
    
    def get_choices(self) -> List[Choice]:
        return CHOICES.get((self.role, self.state), [])
    
    def random_event(self):

        score = (
            self.stats.compliance
            + self.stats.trust
            + self.stats.evidence
            - self.stats.legal_risk
        )

        positive_events = [
            ("📁 Excellent record keeping improves trust.", "good_docs"),
            ("🤝 Communication between tenant and landlord improves.", "trust_up"),
            ("🧹 Tenant keeps the property very clean.", "good_condition"),
        ]

        negative_events = [
            ("🔧 Unexpected repair issue appears in the property.", "maintenance"),
            ("📄 Paperwork confusion causes tension.", "trust_down"),
            ("🪑 Minor furniture damage occurs during the tenancy.", "damage"),
        ]
        # Choose event based on behaviour
        if score >= 3:
            event, event_type = random.choice(positive_events)

        elif score <= -1:
            event, event_type = random.choice(negative_events)
        
        else:
            event, event_type = random.choice(positive_events + negative_events)

        # Apply effects
        if event_type == "trust_up":
            self.stats.trust += 1

        elif event_type == "trust_down":
            self.stats.trust -= 1

        elif event_type == "maintenance":
            self.property.health["interior"] = clamp(
                self.property.health["interior"] - 5,
                0,
                100
            )

        elif event_type == "damage":
            self.property.health["interior"] = clamp(
                self.property.health["interior"] - 10,
                0,
                100
            )

        elif event_type == "good_condition":
            self.property.health["interior"] = clamp(
                self.property.health["interior"] + 5,
                0,
                100
            )

        return event
    
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

        # Advance tenancy timeline only if game continues
        if self.state != GameState.GAME_OVER:
            self.timeline.advance()

       # Tenancy lifecycle events
        self.last_event_message = ""

        # timeline events
        if self.timeline.month == 3:
            self.last_event_message = "📋 Inspection time. The property condition may affect the deposit."

        elif self.timeline.month == 12:
            self.last_event_message = "📅 One year passed. Records and documentation matter more now."

        elif self.timeline.month == 24:
            self.last_event_message = "🏁 Tenancy ending soon. Deposit return and evidence become critical."

        # random events
        if self.state != GameState.GAME_OVER and random.random() < 0.4:
            event = self.random_event()
            self.last_event_message = event

        # refresh weather state
        self.current_weather = self.get_weather_state()

        # Evaluate outcome if game ends
        if self.state == GameState.GAME_OVER:
            self.evaluate_outcome()

        return choice.explanation
       
    def is_game_over(self) -> bool:
        return self.state == GameState.GAME_OVER