import json,tempfile,unittest
from pathlib import Path
from security_assessment.sa06 import *
from security_assessment.runner import run_sa01
from security_assessment.sa02_runner import run_sa02
from security_assessment.sa03_runner import run_sa03
from security_assessment.sa04_runner import run_sa04
from security_assessment.sa05 import run as run5,NaiveDelegatingParticipant
from security_assessment.participants import NaiveParticipant
class S7(unittest.TestCase):
 def setUp(self):self.h=controls()
 def test_claim_not_authority(self):self.assertFalse(verify(canonical())[0])
 def test_support(self):self.assertTrue(verify(self.h[0])[0]);self.assertTrue(verify(self.h[1])[0])
 def test_wrong_emergency_lifecycle(self):self.assertFalse(verify(self.h[2])[0]);self.assertFalse(verify(self.h[3])[0]);self.assertFalse(verify(self.h[4])[0])
 def test_participants(self):self.assertIsNotNone(run(ClaimTrustingParticipant()).finding);self.assertIsNone(run(AuthorityVerifyingParticipant()).finding)
 def test_provenance_and_artifact(self):
  self.assertIn('verification_result',run(ClaimTrustingParticipant()).trace.authority_evaluation)
  with tempfile.TemporaryDirectory() as d:data=json.loads(write_artifact(Path(d)).read_text())
  self.assertEqual(len(data['results']),6)
 def test_regressions(self):self.assertIsNotNone(run_sa01(NaiveParticipant()).finding);self.assertIsNotNone(run_sa02(NaiveParticipant()).finding);self.assertIsNotNone(run_sa03(NaiveParticipant()).finding);self.assertIsNotNone(run_sa04(NaiveParticipant()).finding);self.assertIsNotNone(run5(NaiveDelegatingParticipant()).finding)
