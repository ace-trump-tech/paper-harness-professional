#!/usr/bin/env python3
"""Return bounded, provenance-preserving context from the distilled corpus."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "knowledge" / "index" / "catalog.json"


def _tokens(text: str) -> set[str]:
    tokens = {token.lower() for token in re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]+", text)}
    # A dependency-free fallback for Chinese queries: overlapping character
    # bigrams give useful recall without pretending to be a full tokenizer.
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        tokens.update(run[index:index + 2] for index in range(len(run) - 1))
    return tokens


def _read_entries(include_full_text: bool = False) -> Iterable[tuple[dict, Path, str]]:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    for entry in catalog["entries"]:
        path = (CATALOG.parent / entry["path"]).resolve()
        if path.exists() and path.is_file():
            yield entry, path, path.read_text(encoding="utf-8", errors="replace")
    if include_full_text:
        for path in sorted((ROOT / "papers" / "text").glob("*.txt")):
            yield {"kind": "full-text", "tags": ["paper", "page-marked"]}, path, path.read_text(encoding="utf-8", errors="replace")


def search(query: str, limit: int = 6, max_chars: int = 1800, include_full_text: bool = False) -> list[dict]:
    wanted = _tokens(query)
    ranked = []
    for entry, path, text in _read_entries(include_full_text=include_full_text):
        haystack = _tokens(path.stem + " " + text)
        score = len(wanted & haystack)
        if score:
            ranked.append((score, entry, path, text))
    ranked.sort(key=lambda item: (-item[0], str(item[2])))
    results = []
    for score, entry, path, text in ranked[:limit]:
        lower = text.lower()
        hit = next((lower.find(token.lower()) for token in wanted if lower.find(token.lower()) >= 0), 0)
        start = max(0, hit - max_chars // 3)
        snippet = text[start:start + max_chars].strip()
        results.append({"score": score, "source": str(path.relative_to(ROOT)), "kind": entry["kind"], "tags": entry.get("tags", []), "snippet": snippet})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--max-chars", type=int, default=1800)
    parser.add_argument("--include-full-text", action="store_true", help="also search page-marked extracted PDFs")
    parser.add_argument("--prompt", action="store_true", help="emit a ready-to-paste agent context")
    args = parser.parse_args()
    results = search(args.query, args.limit, args.max_chars, args.include_full_text)
    if args.prompt:
        print("You are a power-grid embodied-intelligence research assistant. Cite only the sources below.\n")
        print("QUESTION: " + args.query + "\n")
        for index, result in enumerate(results, start=1):
            print(f"[{index}] {result['source']} ({result['kind']})\n{result['snippet']}\n")
        print("Return claims, evidence paths, assumptions, unknowns, next actions and human decisions.")
    else:
        print(json.dumps({"query": args.query, "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
