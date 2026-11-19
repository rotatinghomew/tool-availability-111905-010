import csv
from pathlib import Path
import unittest

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

class SourceRecords(unittest.TestCase):
    def test_synthetic_tables_are_well_formed(self):
        paths = sorted(FIXTURES.glob("*.csv"))
        self.assertGreaterEqual(len(paths), 3)
        for path in paths:
            with self.subTest(table=path.name), path.open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source)
                rows = list(reader)
                self.assertTrue(reader.fieldnames)
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))
                if "id" in reader.fieldnames:
                    ids = [row["id"] for row in rows]
                    self.assertEqual(len(ids), len(set(ids)))

    def test_business_references(self):
        tables = {}
        for path in FIXTURES.glob("*.csv"):
            with path.open(encoding="utf-8", newline="") as source:
                tables[path.stem] = list(csv.DictReader(source))
        links = (
            ('certificates', 'asset', 'assets', 'id'),
            ('certificates', 'use', 'uses', 'id'),
            ('requests', 'use', 'uses', 'id'),
            ('service_events', 'asset', 'assets', 'id'),
            ('service_events', 'parent', 'service_events', 'id'),
            ('moves', 'leg', 'legs', 'id'),
            ('moves', 'asset', 'assets', 'id'),
            ('moves', 'protects', 'requests', 'id'),
            ('moves', 'prior', 'moves', 'id'),
        )
        for child, field, parent, key in links:
            with self.subTest(table=child, field=field):
                known = {row[key] for row in tables[parent]}
                for row in tables[child]:
                    if row[field]:
                        self.assertIn(row[field], known)
