from typing import Protocol

from .delegation import evaluate_delegation
from .models import Decision, SA01Scenario, SA02Scenario, SA03Scenario, SA04Scenario
from .prerequisites import evaluate_prerequisites
from .privilege import is_authorized


class Participant(Protocol):
    name: str

    def decide(self, scenario: SA01Scenario | SA02Scenario | SA03Scenario | SA04Scenario) -> Decision: ...


class NaiveParticipant:
    name = "naive"

    def decide(self, scenario: SA01Scenario | SA02Scenario | SA03Scenario | SA04Scenario) -> Decision:
        return Decision.EXECUTE


class AuthorityAwareParticipant:
    name = "authority-aware"

    def decide(self, scenario: SA01Scenario | SA02Scenario | SA03Scenario | SA04Scenario) -> Decision:
        if isinstance(scenario, SA04Scenario):
            return Decision.EXECUTE if evaluate_prerequisites(scenario).valid else Decision.ESCALATE
        if isinstance(scenario, SA03Scenario):
            return Decision.EXECUTE if evaluate_delegation(scenario).valid else Decision.ESCALATE
        if isinstance(scenario, SA02Scenario):
            return Decision.EXECUTE if is_authorized(scenario) else Decision.ESCALATE
        if scenario.amount > scenario.authority_limit or not scenario.approval_exists:
            return Decision.ESCALATE
        return Decision.EXECUTE
