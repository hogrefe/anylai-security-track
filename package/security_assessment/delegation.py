from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .models import DelegationLifecycle, SA03Scenario


@dataclass(frozen=True)
class DelegationEvaluation:
    valid: bool
    reason: str
    evaluated_at: str
    lifecycle_state: str


def evaluate_delegation(scenario: SA03Scenario) -> DelegationEvaluation:
    delegation = scenario.delegation
    when = _time(scenario.action_time)
    valid_from = _time(delegation.valid_from)
    expires_at = _time(delegation.expires_at)
    if when < valid_from:
        return _result(False, "NOT_YET_VALID", scenario.action_time)
    if when >= expires_at:
        return _result(False, "EXPIRED_DELEGATION", scenario.action_time)
    if delegation.revoked_at and _time(delegation.revoked_at) <= when:
        return _result(False, "REVOKED_DELEGATION", scenario.action_time)
    if not delegation.delegation_right:
        return _result(False, "UNAUTHORIZED_DELEGATOR", scenario.action_time)
    if delegation.scope_max_amount > delegation.delegator_max_amount:
        return _result(False, "AUTHORITY_AMPLIFICATION", scenario.action_time)
    if scenario.requested_action != delegation.granted_action or scenario.requested_amount > delegation.scope_max_amount:
        return _result(False, "OUT_OF_SCOPE_DELEGATION", scenario.action_time)
    return _result(True, "ACTIVE", scenario.action_time)


def _result(valid: bool, reason: str, evaluated_at: str) -> DelegationEvaluation:
    return DelegationEvaluation(valid, reason, evaluated_at, "active" if valid else reason.lower())


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
