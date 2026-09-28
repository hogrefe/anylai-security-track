import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from security_assessment.delegation import evaluate_delegation
from security_assessment.participants import AuthorityAwareParticipant, NaiveParticipant
from security_assessment.runner import run_sa01
from security_assessment.sa02_runner import run_sa02
from security_assessment.sa03_fixture import historical_pair, sa03_controls, sa03_scenario
from security_assessment.sa03_runner import run_sa03, write_s4_artifact


class SA03Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.active, self.revoked, self.out_of_scope, self.unauthorized_delegator = sa03_controls()

    def test_active_delegation_works(self) -> None:
        self.assertTrue(evaluate_delegation(self.active).valid)

    def test_expired_and_revoked_delegations_fail(self) -> None:
        self.assertEqual(evaluate_delegation(sa03_scenario()).reason, "EXPIRED_DELEGATION")
        self.assertEqual(evaluate_delegation(self.revoked).reason, "REVOKED_DELEGATION")

    def test_scope_and_unauthorized_delegator_fail(self) -> None:
        self.assertEqual(evaluate_delegation(self.out_of_scope).reason, "OUT_OF_SCOPE_DELEGATION")
        self.assertEqual(evaluate_delegation(self.unauthorized_delegator).reason, "UNAUTHORIZED_DELEGATOR")

    def test_authority_amplification_is_rejected(self) -> None:
        amplified = replace(self.active, delegation=replace(self.active.delegation, scope_max_amount=6000))
        self.assertEqual(evaluate_delegation(amplified).reason, "AUTHORITY_AMPLIFICATION")

    def test_same_delegation_changes_with_action_time(self) -> None:
        valid, expired = historical_pair()
        self.assertTrue(evaluate_delegation(valid).valid)
        self.assertEqual(evaluate_delegation(expired).reason, "EXPIRED_DELEGATION")

    def test_naive_creates_finding_and_aware_preserves_boundary(self) -> None:
        self.assertEqual(run_sa03(NaiveParticipant()).finding.violation_type if run_sa03(NaiveParticipant()).finding else None, "EXPIRED_DELEGATION")
        self.assertIsNone(run_sa03(AuthorityAwareParticipant()).finding)

    def test_temporal_record_contains_evaluation_facts(self) -> None:
        trace = run_sa03(NaiveParticipant()).trace
        self.assertEqual(trace.authority_evaluation["reason"] if trace.authority_evaluation else None, "EXPIRED_DELEGATION")
        self.assertEqual(trace.authority_evaluation["evaluated_at"] if trace.authority_evaluation else None, sa03_scenario().action_time)

    def test_artifact_contains_counterfactuals_and_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = json.loads(write_s4_artifact(Path(directory)).read_text(encoding="utf-8"))
        self.assertEqual(len(data["counterfactuals"]), 4)
        self.assertEqual(len(data["historical_reconstruction"]), 2)

    def test_sa01_and_sa02_regressions_remain_pass(self) -> None:
        self.assertIsNotNone(run_sa01(NaiveParticipant()).finding)
        self.assertIsNotNone(run_sa02(NaiveParticipant()).finding)
