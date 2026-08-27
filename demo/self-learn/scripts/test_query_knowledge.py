#!/usr/bin/env python3
import unittest

from query_knowledge import search


class KnowledgeQueryTest(unittest.TestCase):
    def test_chinese_query_returns_distilled_sources(self):
        results = search("储能 安全 门控 预测误差", limit=10)
        sources = {item["source"] for item in results}
        self.assertTrue(any("innovation-bank.md" in source for source in sources))
        self.assertTrue(any("commonpower" in source or "power-grid-literature-run" in source for source in sources))


if __name__ == "__main__":
    unittest.main()
