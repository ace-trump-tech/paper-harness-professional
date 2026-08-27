#!/usr/bin/env zsh
set -euo pipefail

root_dir="${0:A:h:h}"
raw_dir="$root_dir/papers/raw"
mkdir -p "$raw_dir"

download() {
  local name="$1"
  local url="$2"
  local partial="$raw_dir/.${name}.part"
  curl -fL --continue-at - --retry 3 --retry-delay 3 --connect-timeout 20 \
    -o "$partial" "$url"
  python3 - "$partial" <<'PY'
from pathlib import Path
from pypdf import PdfReader
import sys

path = Path(sys.argv[1])
if not PdfReader(str(path)).pages:
    raise RuntimeError(f"No readable pages in {path}")
PY
  mv "$partial" "$raw_dir/$name"
}

download powergym.pdf https://arxiv.org/pdf/2109.03970
download powergridworld.pdf https://arxiv.org/pdf/2111.05969
download gym-anm.pdf https://arxiv.org/pdf/2103.07932
download commonpower.pdf https://arxiv.org/pdf/2406.03231
download safe-rl-power-system-control-review.pdf https://arxiv.org/pdf/2407.00681
download safe-rl-modern-power-systems-review.pdf https://arxiv.org/pdf/2407.00304
download foundation-models-power-systems.pdf https://arxiv.org/pdf/2312.07044
download x-gridagent.pdf https://arxiv.org/pdf/2512.20789
download llm-multi-agent-power-electronics-control.pdf https://arxiv.org/pdf/2406.12628
download powernet.pdf https://www.osti.gov/servlets/purl/1877584
