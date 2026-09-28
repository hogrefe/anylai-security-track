from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .models import SA04Scenario


ACCEPTED_SOURCES = {"manager", "quote_service"}


@dataclass(frozen=True)
class PrerequisiteEvaluation:
    valid: bool
    reason: str
    evaluated_at: str


def evaluate_prerequisites(scenario: SA04Scenario) -> PrerequisiteEvaluation:
    when = _time(scenario.action_time)
    for requirement_id, requirement_type in scenario.required_prerequisites:
        candidates = [item for item in scenario.prerequisites if item.requirement_id == requirement_id]
        if not candidates:
            return _result(False, "MISSING_APPROVAL", scenario.action_time)
        item = candidates[0]
        if item.status != "valid" or item.requirement_type != requirement_type:
            return _result(False, "INVALID_PREREQUISITE", scenario.action_time)
        if item.source not in ACCEPTED_SOURCES:
            return _result(False, "UNTRUSTED_EVIDENCE", scenario.action_time)
        if item.required_for_action != scenario.action or item.transaction_id != scenario.transaction_id:
            return _result(False, "UNBOUND_EVIDENCE", scenario.action_time)
        if when < _time(item.valid_from) or when >= _time(item.expires_at):
            return _result(False, "EXPIRED_APPROVAL", scenario.action_time)
    return _result(True, "COMPLETE", scenario.action_time)


def _result(valid: bool, reason: str, evaluated_at: str) -> PrerequisiteEvaluation:
    return PrerequisiteEvaluation(valid, reason, evaluated_at)


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
