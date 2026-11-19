import csv
from pathlib import Path
import unittest


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
HEADERS = {'stock': ['id', 'kind', 'depot'], 'parts': ['kit', 'unit'], 'certifications': ['entity', 'purpose', 'site', 'start', 'end'], 'movements': ['id', 'unit', 'kind', 'site', 'lower', 'upper', 'received'], 'requests': ['id', 'site', 'purpose', 'start', 'end', 'disposition', 'observed'], 'reservations': ['id', 'request', 'entity', 'start', 'end', 'status'], 'work_orders': ['id', 'kind', 'unit', 'source', 'dest', 'planned', 'status'], 'routes': ['source', 'dest', 'kind', 'min_hours'], 'amendments': ['id', 'replaces', 'field', 'value', 'recorded']}
LINKS = [('parts', 'unit', 'stock', 'id'), ('movements', 'unit', 'stock', 'id'), ('reservations', 'request', 'requests', 'id'), ('amendments', 'replaces', 'movements', 'id')]


def read(name):
    with (FIXTURES / (name + ".csv")).open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        return reader.fieldnames, list(reader)


class SourceRecords(unittest.TestCase):
    def test_records_match_source_columns(self):
        for name, expected in HEADERS.items():
            with self.subTest(table=name):
                header, rows = read(name)
                self.assertEqual(header, expected)
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))
                if "id" in header:
                    ids = [row["id"] for row in rows]
                    self.assertTrue(all(ids))
                    self.assertEqual(len(ids), len(set(ids)))

    def test_record_references_exist(self):
        for source, field, target, key in LINKS:
            with self.subTest(table=source, column=field):
                _, source_rows = read(source)
                _, target_rows = read(target)
                keys = {row[key] for row in target_rows}
                self.assertTrue(all(row[field] in keys for row in source_rows))
