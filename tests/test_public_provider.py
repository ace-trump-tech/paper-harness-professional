import unittest
from unittest.mock import patch

from paper_harness.providers.public import OpenAlexProvider


class PublicProviderTest(unittest.TestCase):
    def test_openalex_handles_null_primary_source_and_author(self):
        payload = {"results": [{"id": "https://openalex.org/W1", "title": "Grid control", "authorships": [{"author": None}], "primary_location": {"source": None}, "publication_year": 2025, "cited_by_count": 2}]}
        with patch("paper_harness.providers.public._get_json", return_value=payload):
            record = list(OpenAlexProvider().search("grid", limit=1))[0]
        self.assertEqual(record.venue, "")
        self.assertEqual(record.authors, [""])


if __name__ == "__main__":
    unittest.main()
