import json
import tempfile
import unittest
from pathlib import Path

from security_assessment.participants import AuthorityAwareParticipant, NaiveParticipant
from security_assessment.sa02_fixture import sa02_controls, sa02_scenario
from security_assessment.sa02_runner import run_sa02, write_s3_artifact
from security_assessment.runner import run_sa01


class SA02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.r1, self.r2, self.r3 = sa02_controls()

    def test_lower_role_naive_execution_creates_privilege_finding(self) -> None:
        result = run_sa02(NaiveParticipant())
        self.assertTrue(result.trace.consequential_attempted)
        self.assertEqual(result.finding.violation_type if result.finding else None, "PRIVILEGE_ESCALATION")

    def test_authority_aware_participant_prevents_canonical_violation(self) -> None:
        result = run_sa02(AuthorityAwareParticipant())
        self.assertFalse(result.trace.consequential_attempted)
        self.assertIsNone(result.finding)

    def test_correct_higher_role_removes_false_positive(self) -> None:
        result = run_sa02(NaiveParticipant(), self.r1)
        self.assertTrue(result.trace.consequential_attempted)
        self.assertIsNone(result.finding)

    def test_valid_scoped_delegation_allows_action(self) -> None:
        result = run_sa02(NaiveParticipant(), self.r2)
        self.assertIsNone(result.finding)

    def test_invalid_delegation_does_not_elevate_privilege(self) -> None:
        result = run_sa02(NaiveParticipant(), self.r3)
        self.assertIsNotNone(result.finding)

    def test_finding_requires_executed_privileged_action(self) -> None:
        result = run_sa02(AuthorityAwareParticipant())
        self.assertEqual(result.trace.actual_consequence, "action_not_executed")
        self.assertIsNone(result.finding)

    def test_sa01_regression_is_unchanged(self) -> None:
        self.assertIsNotNone(run_sa01(NaiveParticipant()).finding)

    def test_artifact_contains_canonical_controls_and_trace_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_s3_artifact(Path(directory))
            data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["canonical"]["scenario"]["scenario_id"], sa02_scenario().scenario_id)
        self.assertEqual(len(data["counterfactuals"]), 3)
        self.assertEqual(data["canonical"]["finding"]["trace_reference"], "trace:SA-02-privilege-escalation:naive")
