import json
import tempfile
import unittest
from pathlib import Path

from security_assessment.counterfactuals import changed_fields, sa01_counterfactuals
from security_assessment.fixture import sa01_scenario
from security_assessment.participants import NaiveParticipant
from security_assessment.runner import run_sa01, run_sa01_scenario, write_s2_artifact


class SA01CounterfactualTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = {case.case_id: case for case in sa01_counterfactuals()}

    def test_canonical_s1_behavior_is_preserved(self) -> None:
        result = run_sa01(NaiveParticipant())
        self.assertEqual(result.scenario, sa01_scenario())
        self.assertIsNotNone(result.finding)

    def test_valid_authority_alone_does_not_hide_missing_approval(self) -> None:
        result = run_sa01_scenario(NaiveParticipant(), self.cases["CF-01"].scenario)
        self.assertIsNotNone(result.finding)
        self.assertEqual(self.cases["CF-01"].scenario.authority_limit, 7500)

    def test_valid_approval_alone_does_not_hide_excess_amount(self) -> None:
        result = run_sa01_scenario(NaiveParticipant(), self.cases["CF-02"].scenario)
        self.assertIsNotNone(result.finding)
        self.assertTrue(self.cases["CF-02"].scenario.approval_exists)

    def test_stimulus_removal_is_distinct_from_authority_violation(self) -> None:
        result = run_sa01_scenario(NaiveParticipant(), self.cases["CF-03"].scenario)
        self.assertIsNone(self.cases["CF-03"].scenario.stimulus)
        self.assertIsNotNone(result.finding)

    def test_authorized_within_scope_action_is_not_flagged(self) -> None:
        result = run_sa01_scenario(NaiveParticipant(), self.cases["CF-04"].scenario)
        self.assertTrue(result.trace.consequential_attempted)
        self.assertIsNone(result.finding)

    def test_cases_change_only_the_declared_variable_from_their_base(self) -> None:
        canonical = sa01_scenario()
        cf02 = self.cases["CF-02"].scenario
        bases = {"CF-01": canonical, "CF-02": canonical, "CF-03": canonical, "CF-04": cf02}
        for case_id, case in self.cases.items():
            self.assertEqual(changed_fields(bases[case_id], case.scenario), {case.changed_variable})

    def test_artifact_records_ground_truth_and_finding_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_s2_artifact(Path(directory))
            rows = json.loads(path.read_text(encoding="utf-8"))["counterfactuals"]
        self.assertEqual([row["counterfactual_id"] for row in rows], ["CF-01", "CF-02", "CF-03", "CF-04"])
        self.assertFalse(rows[3]["finding_generated"])
