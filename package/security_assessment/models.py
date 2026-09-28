from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StimulusSource(str, Enum):
    UNTRUSTED_TOOL_OUTPUT = "UNTRUSTED_TOOL_OUTPUT"


class TrustLevel(str, Enum):
    UNTRUSTED = "UNTRUSTED"


class Decision(str, Enum):
    EXECUTE = "EXECUTE"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class AdversarialStimulus:
    source: StimulusSource
    trust_level: TrustLevel
    content: str
    intended_influence: str


@dataclass(frozen=True)
class SecurityFinding:
    finding_id: str
    test_family: str
    scenario_id: str
    participant: str
    precondition: str
    adversarial_stimulus: str
    authority_ground_truth: str
    expected_behavior: str
    observed_behavior: str
    consequential_action: str
    violation_type: str
    trace_reference: str
    reproduction_reference: str


@dataclass(frozen=True)
class SA01Scenario:
    scenario_id: str
    principal: str
    action: str
    amount: int
    authority_limit: int
    approval_exists: bool
    stimulus: AdversarialStimulus | None


@dataclass(frozen=True)
class Delegation:
    action: str
    valid: bool
    status: str


@dataclass(frozen=True)
class SA02Scenario:
    scenario_id: str
    principal: str
    actor_role: str
    action: str
    required_role: str
    delegation: Delegation | None
    stimulus: AdversarialStimulus


@dataclass(frozen=True)
class DelegationLifecycle:
    delegator: str
    delegate: str
    granted_action: str
    scope_max_amount: int
    issued_at: str
    valid_from: str
    expires_at: str
    revoked_at: str | None
    delegation_right: bool
    delegator_max_amount: int


@dataclass(frozen=True)
class SA03Scenario:
    scenario_id: str
    delegation: DelegationLifecycle
    requested_action: str
    requested_amount: int
    action_time: str
    stimulus: AdversarialStimulus


@dataclass(frozen=True)
class Prerequisite:
    requirement_id: str
    requirement_type: str
    required_for_action: str
    status: str
    source: str
    valid_from: str
    expires_at: str
    reference: str
    transaction_id: str


@dataclass(frozen=True)
class SA04Scenario:
    scenario_id: str
    principal: str
    action: str
    amount: int
    transaction_id: str
    action_time: str
    required_prerequisites: tuple[tuple[str, str], ...]
    prerequisites: tuple[Prerequisite, ...]
    stimulus: AdversarialStimulus


@dataclass(frozen=True)
class Trace:
    trace_id: str
    participant: str
    decision: Decision
    attempted_action: str
    consequential_attempted: bool
    actual_consequence: str
    authority_evaluation: dict[str, object] | None = None


@dataclass(frozen=True)
class AssessmentResult:
    scenario: SA01Scenario | SA02Scenario | SA03Scenario | SA04Scenario
    participant: str
    trace: Trace
    finding: SecurityFinding | None
