import json
import tempfile
import unittest
from pathlib import Path

from security_assessment.participants import AuthorityAwareParticipant, NaiveParticipant
from security_assessment.runner import run_sa01
from security_assessment.sa02_runner import run_sa02
from security_assessment.sa03_runner import run_sa03
from security_assessment.sa04_fixture import sa04_controls, sa04_scenario
from security_assessment.sa04_runner import run_sa04, write_s5_artifact


class SA04Tests(unittest.TestCase):
    def setUp(self) -> None: self.valid, self.expired, self.wrong, self.assertion, self.partial = sa04_controls()
    def test_valid_authority_alone_is_not_sufficient(self) -> None: self.assertIsNotNone(run_sa04(NaiveParticipant()).finding)
    def test_aware_blocks_missing_prerequisite(self) -> None: self.assertIsNone(run_sa04(AuthorityAwareParticipant()).finding)
    def test_valid_approval_allows_action(self) -> None: self.assertIsNone(run_sa04(NaiveParticipant(), self.valid).finding)
    def test_expired_and_wrong_transaction_do_not_allow_action(self) -> None:
        self.assertEqual(run_sa04(NaiveParticipant(), self.expired).finding.violation_type if run_sa04(NaiveParticipant(), self.expired).finding else None, "EXPIRED_APPROVAL")
        self.assertEqual(run_sa04(NaiveParticipant(), self.wrong).finding.violation_type if run_sa04(NaiveParticipant(), self.wrong).finding else None, "UNBOUND_EVIDENCE")
    def test_assertion_and_partial_evidence_do_not_satisfy_ground_truth(self) -> None:
        self.assertEqual(run_sa04(NaiveParticipant(), self.assertion).finding.violation_type if run_sa04(NaiveParticipant(), self.assertion).finding else None, "MISSING_APPROVAL")
        self.assertEqual(run_sa04(NaiveParticipant(), self.partial).finding.violation_type if run_sa04(NaiveParticipant(), self.partial).finding else None, "MISSING_APPROVAL")
    def test_trace_records_pre_action_evidence_facts(self) -> None:
        trace = run_sa04(NaiveParticipant()).trace
        self.assertEqual(trace.authority_evaluation["provided_prerequisites"] if trace.authority_evaluation else None, [])
    def test_artifact_contains_controls(self) -> None:
        with tempfile.TemporaryDirectory() as directory: data = json.loads(write_s5_artifact(Path(directory)).read_text(encoding="utf-8"))
        self.assertEqual(len(data["counterfactuals"]), 5)
    def test_prior_regressions_remain_pass(self) -> None:
        self.assertIsNotNone(run_sa01(NaiveParticipant()).finding)
        self.assertIsNotNone(run_sa02(NaiveParticipant()).finding)
        self.assertIsNotNone(run_sa03(NaiveParticipant()).finding)
