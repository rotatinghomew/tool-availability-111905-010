import csv
import unittest
from pathlib import Path


class FixtureTests(unittest.TestCase):
    def test_reporting_fixture_contains_sources_metrics_and_subscriptions(self):
        path = Path(__file__).parents[1] / "fixtures" / "reporting.csv"
        with path.open(encoding="utf-8", newline="") as source:
            rows = list(csv.DictReader(source))
        kinds = {row["record_type"] for row in rows}
        self.assertTrue({"event", "metric", "subscription", "delivery"} <= kinds)
        self.assertEqual(len(rows), len({row["record_id"] for row in rows}))


if __name__ == "__main__":
    unittest.main()
