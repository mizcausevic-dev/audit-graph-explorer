import unittest

from src.audit_graph_report import build_report, build_indexes, find_path, load_snapshot


class AuditGraphReportTest(unittest.TestCase):
    def test_summary_counts_stay_stable(self):
        report = build_report()
        self.assertEqual(report["summary"]["node_count"], 23)
        self.assertEqual(report["summary"]["edge_count"], 37)
        self.assertEqual(report["summary"]["open_exceptions"], 2)

    def test_path_reaches_tier_zero_asset(self):
        snapshot = load_snapshot()
        nodes, adjacency = build_indexes(snapshot)
        path = find_path(nodes, adjacency, "exception-233", "asset-admin-console")
        self.assertEqual(path[0]["id"], "exception-233")
        self.assertEqual(path[-1]["id"], "asset-admin-console")
        self.assertGreaterEqual(len(path), 2)


if __name__ == "__main__":
    unittest.main()

