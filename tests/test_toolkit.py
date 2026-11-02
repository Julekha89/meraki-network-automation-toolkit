import tempfile
import unittest
from pathlib import Path
from src.meraki_toolkit import build_report, save_csv, request_json

class ReportTests(unittest.TestCase):
    def test_join(self):
        rows = build_report([{'name':'MX','serial':'X','model':'MX68'}], [{'serial':'X','uplinks':[{'interface':'wan1','status':'active'}]}])
        self.assertEqual(rows[0]['status'], 'active')
        self.assertEqual(rows[0]['interface'], 'wan1')

    def test_missing_uplinks(self):
        rows = build_report([{'serial':'Y'}], [])
        self.assertEqual(rows[0]['status'], 'not_applicable')

    def test_empty_inventory(self):
        self.assertEqual(build_report([], []), [])

    def test_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'out.csv'
            save_csv(build_report([{'serial':'Y'}], []), target)
            self.assertIn('not_applicable', target.read_text())

    def test_https_required(self):
        with self.assertRaises(ValueError):
            request_json('organizations', 'dummy', base_url='http://example.com')

if __name__ == '__main__':
    unittest.main()
