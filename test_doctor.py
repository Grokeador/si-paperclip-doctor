"""Automated verification suite for SI-Paperclip-Doctor against Paperclip AI workspace bugs."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from si_paperclip_doctor import (
    repair_workspace,
    rollback_workspace,
    scan_workspace,
    seed_realistic_demo_workspace,
)


class SiPaperclipDoctorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="si_paperclip_test_"))
        self.ws = seed_realistic_demo_workspace(self.tmp / "paperclip_ws")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_scan_detects_all_real_paperclip_issues(self) -> None:
        audit = scan_workspace(self.ws)
        self.assertTrue(audit["ok"])
        self.assertEqual(audit["issue_count"], 5)
        ids = {i["id"] for i in audit["issues"]}
        self.assertIn("ACCOUNTING_RECOVERY_DEADLOCK", ids)
        self.assertIn("GOVERNANCE_CONNECTION_INTENT", ids)
        self.assertIn("RESERVED_DOC_KEY_LIST", ids)
        self.assertIn("SHARED_BLOCKER_EXPONENTIAL", ids)
        self.assertIn("CLOUD_API_SPEND_EXPOSED", ids)

    def test_repair_fixes_all_issues_and_configures_zero_cost_ollama(self) -> None:
        res = repair_workspace(self.ws, local_model="qwen2.5-coder:14b")
        self.assertTrue(res["ok"])
        self.assertEqual(res["remaining_issues"], 0)

        gov = json.loads((self.ws / "company_settings.json").read_text(encoding="utf-8"))
        self.assertNotIn("connection_intent", gov.get("interaction_governance", {}))
        self.assertEqual(gov.get("default_provider"), "http://127.0.0.1:11434/v1")

        board = json.loads((self.ws / "tasks_board.json").read_text(encoding="utf-8"))
        t101 = next(t for t in board["tasks"] if t["id"] == "T-101")
        self.assertEqual(t101["doc_key"], "doc_list")
        t104 = next(t for t in board["tasks"] if t["id"] == "T-104")
        self.assertNotIn("T-104", t104["blocked_by"])

        harness = json.loads((self.ws / "paperclip_local_harness.json").read_text(encoding="utf-8"))
        self.assertEqual(harness["monthly_budget_usd"], 0.0)
        self.assertTrue(harness["hard_stop_on_paid_api"])
        self.assertTrue((self.ws / ".paperclip.local.env").exists())

    def test_sha256_rollback_restores_exact_state(self) -> None:
        repair_workspace(self.ws)
        rb = rollback_workspace(self.ws)
        self.assertTrue(rb["ok"])
        self.assertGreaterEqual(rb["restored_files"], 3)
        self.assertFalse((self.ws / "paperclip_local_harness.json").exists())
        post_rb = scan_workspace(self.ws)
        self.assertEqual(post_rb["issue_count"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
