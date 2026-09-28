import json
import tempfile
import unittest
from pathlib import Path

from security_assessment.fixture import sa01_scenario
from security_assessment.models import StimulusSource, TrustLevel
from security_assessment.participants import AuthorityAwareParticipant, NaiveParticipant
from security_assessment.runner import run_sa01, write_s1_artifact


class SA01Tests(unittest.TestCase):
    def test_stimulus_is_untrusted_tool_output(self) -> None:
        stimulus = sa01_scenario().stimulus
        self.assertEqual(stimulus.source, StimulusSource.UNTRUSTED_TOOL_OUTPUT)
        self.assertEqual(stimulus.trust_level, TrustLevel.UNTRUSTED)

    def test_naive_participant_creates_unauthorized_finding(self) -> None:
        result = run_sa01(NaiveParticipant())
        self.assertTrue(result.trace.consequential_attempted)
        self.assertEqual(result.trace.actual_consequence, "order_placed")
        self.assertIsNotNone(result.finding)

    def test_authority_aware_participant_preserves_authority(self) -> None:
        result = run_sa01(AuthorityAwareParticipant())
        self.assertFalse(result.trace.consequential_attempted)
        self.assertEqual(result.trace.actual_consequence, "action_not_executed")
        self.assertIsNone(result.finding)

    def test_finding_references_observable_trace_and_violation(self) -> None:
        finding = run_sa01(NaiveParticipant()).finding
        assert finding is not None
        self.assertEqual(finding.violation_type, "UNAUTHORIZED_CONSEQUENTIAL_ACTION")
        self.assertEqual(finding.trace_reference, "trace:SA-01-untrusted-tool-output:naive")

    def test_artifact_reconstructs_scenario_stimulus_trace_and_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = write_s1_artifact(Path(directory))
            data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["scenario"]["scenario_id"], "SA-01-untrusted-tool-output")
        self.assertEqual(data["stimulus"]["source"], "UNTRUSTED_TOOL_OUTPUT")
        self.assertEqual(data["results"][0]["finding"]["violation_type"], "UNAUTHORIZED_CONSEQUENTIAL_ACTION")
        self.assertIsNone(data["results"][1]["finding"])
