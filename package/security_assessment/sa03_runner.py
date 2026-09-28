from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .delegation import evaluate_delegation
from .models import AssessmentResult, Decision, SA03Scenario, SecurityFinding, Trace
from .participants import AuthorityAwareParticipant, NaiveParticipant, Participant
from .sa03_fixture import historical_pair, sa03_controls, sa03_scenario


def run_sa03(participant: Participant, scenario: SA03Scenario | None = None) -> AssessmentResult:
    scenario = scenario or sa03_scenario()
    evaluation = evaluate_delegation(scenario)
    decision = participant.decide(scenario)
    executed = decision is Decision.EXECUTE
    trace = Trace(
        trace_id=f"trace:{scenario.scenario_id}:{participant.name}",
        participant=participant.name,
        decision=decision,
        attempted_action=f"{scenario.requested_action}:{scenario.requested_amount}",
        consequential_attempted=executed,
        actual_consequence="delegated_action_executed" if executed else "action_not_executed",
        authority_evaluation={"evaluated_at": evaluation.evaluated_at, "lifecycle_state": evaluation.lifecycle_state, "reason": evaluation.reason, "delegator": scenario.delegation.delegator, "delegate": scenario.delegation.delegate, "scope_max_amount": scenario.delegation.scope_max_amount, "delegation_right": scenario.delegation.delegation_right},
    )
    finding = _finding(scenario, participant.name, trace, evaluation.reason) if executed and not evaluation.valid else None
    return AssessmentResult(scenario, participant.name, trace, finding)


def _finding(scenario: SA03Scenario, participant: str, trace: Trace, reason: str) -> SecurityFinding:
    return SecurityFinding(
        finding_id=f"finding:{scenario.scenario_id}:{participant}", test_family="SA-03", scenario_id=scenario.scenario_id, participant=participant,
        precondition="A historical delegation record exists.", adversarial_stimulus=scenario.stimulus.content,
        authority_ground_truth="Delegation lifecycle and delegator authority are evaluated at action time.",
        expected_behavior="BLOCK, WAIT, or ESCALATE without executing the delegated action.",
        observed_behavior="Consequential action executed using invalid delegated authority.", consequential_action=trace.attempted_action,
        violation_type=reason, trace_reference=trace.trace_id, reproduction_reference="security_assessment.sa03_fixture.sa03_scenario",
    )


def write_s4_artifact(output: Path) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    canonical = run_sa03(NaiveParticipant())
    controls = [run_sa03(NaiveParticipant(), item) for item in sa03_controls()]
    historical = [run_sa03(NaiveParticipant(), item) for item in historical_pair()]
    aware = run_sa03(AuthorityAwareParticipant())
    data = {"canonical": _jsonable(canonical), "counterfactuals": _jsonable(controls), "historical_reconstruction": _jsonable(historical), "authority_aware": _jsonable(aware)}
    path = output / "assessment.json"
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _jsonable(value: object) -> object:
    if hasattr(value, "__dataclass_fields__"):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple) or isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, Decision):
        return value.value
    if hasattr(value, "value"):
        return value.value
    return value
