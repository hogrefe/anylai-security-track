import json,tempfile,unittest
from pathlib import Path
from security_assessment.sa05 import *
from security_assessment.runner import run_sa01
from security_assessment.sa02_runner import run_sa02
from security_assessment.sa03_runner import run_sa03
from security_assessment.sa04_runner import run_sa04
from security_assessment.participants import NaiveParticipant
class S6(unittest.TestCase):
 def setUp(self): self.c=controls()
 def test_scope_amplification(self): self.assertEqual(evaluate(canonical())[1],'DELEGATION_SCOPE_AMPLIFICATION')
 def test_equal_scope_removes_delegation_amplification(self): self.assertEqual(evaluate(self.c[0])[1],'CHAIN_AUTHORITY_AMPLIFICATION')
 def test_narrower_works(self): self.assertTrue(evaluate(self.c[1])[0])
 def test_action_and_right(self): self.assertEqual(evaluate(self.c[2])[1],'DELEGATION_ACTION_AMPLIFICATION'); self.assertEqual(evaluate(self.c[3])[1],'UNAUTHORIZED_REDELEGATION')
 def test_three_hop_preserves_narrowest(self): self.assertEqual(evaluate(self.c[4])[1],'DELEGATION_SCOPE_AMPLIFICATION')
 def test_naive_and_aware(self): self.assertIsNotNone(run(NaiveDelegatingParticipant()).finding); self.assertIsNone(run(AuthorityAwareDelegatingParticipant()).finding)
 def test_record_and_artifact(self):
  self.assertIn('effective_authority',run(NaiveDelegatingParticipant()).trace.authority_evaluation)
  with tempfile.TemporaryDirectory() as d: data=json.loads(write_artifact(Path(d)).read_text())
  self.assertEqual(len(data['results']),6)
 def test_regressions(self): self.assertIsNotNone(run_sa01(NaiveParticipant()).finding); self.assertIsNotNone(run_sa02(NaiveParticipant()).finding); self.assertIsNotNone(run_sa03(NaiveParticipant()).finding); self.assertIsNotNone(run_sa04(NaiveParticipant()).finding)
