import tempfile,unittest
from pathlib import Path
from security_assessment.s8 import Journal,conditions,execute_condition,rebuild
G='{"decision":"EXECUTE","action":"x","arguments":{}}'
class TestS8(unittest.TestCase):
 def setUp(self):self.d=tempfile.TemporaryDirectory();self.p=Path(self.d.name);self.j=Journal(self.p/"runs.jsonl");self.c=conditions()[0]
 def tearDown(self):self.d.cleanup()
 def test_t1_started(self):execute_condition(self.c,self.j,lambda _:G);self.assertEqual(self.j.records()[0]["status"],"RUN_STARTED")
 def test_t2_raw(self):self.assertEqual(execute_condition(self.c,self.j,lambda _:"no")["raw_response"],"no")
 def test_t3_failed(self):r=execute_condition(self.c,self.j,lambda _:"no");self.assertEqual((r["status"],r["parser_status"]),("RUN_FAILED","FAIL"))
 def test_t4_reconstruct(self):execute_condition(self.c,self.j,lambda _:G);self.assertEqual(rebuild(self.p)["completed_conditions"],1)
 def test_t5_summary(self):execute_condition(self.c,self.j,lambda _:G);a=rebuild(self.p);(self.p/"summary.json").unlink();self.assertEqual(rebuild(self.p),a)
 def test_t6_resume(self):
  execute_condition(self.c,self.j,lambda _:G);self.assertEqual(execute_condition(self.c,self.j,lambda _:(_ for _ in ()).throw(Exception()))["status"],"RUN_COMPLETED")
