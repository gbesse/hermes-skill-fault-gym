import unittest,copy,json
from hermes_skill_fault_gym import run
DEMO={'stock': 10, 'quantity': 3, 'faults': ['none', 'before_write', 'after_write', 'duplicate_delivery', 'stale_snapshot']}
class DomainTests(unittest.TestCase):
 def test_post_write_failure_distinguishes_strategies(self):
  x=run(DEMO)['scenarios'];blind=next(r for r in x if r['fault']=='after_write'and r['strategy']=='blind_retry');safe=next(r for r in x if r['fault']=='after_write'and r['strategy']=='reconcile');self.assertEqual(blind['effects'],2);self.assertEqual(safe['effects'],1)
 def test_stale_snapshot_blocks_reconciliation_strategy(self):
  x=run(DEMO)['scenarios'];self.assertTrue(next(r for r in x if r['fault']=='stale_snapshot'and r['strategy']=='reconcile')['stale_action_blocked'])
 def test_before_write_retry_still_one_effect(self):
  x=run(DEMO)['scenarios'];self.assertTrue(all(r['effects']==1 for r in x if r['fault']=='before_write'))
