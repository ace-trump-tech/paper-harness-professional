#!/usr/bin/env zsh
set -euo pipefail

root_dir="${0:A:h:h}"
code_dir="$root_dir/code"
mkdir -p "$code_dir"

clone_if_missing() {
  local name="$1"
  local url="$2"
  local target="$code_dir/$name"
  if [[ ! -d "$target/.git" ]]; then
    local staging_dir
    staging_dir=$(mktemp -d "$code_dir/.download-${name}.XXXXXX")
    git clone --depth 1 "$url" "$staging_dir/repo"
    git -C "$staging_dir/repo" fsck --no-dangling
    mv "$staging_dir/repo" "$target"
    rmdir "$staging_dir"
  fi
}

clone_if_missing grid2op https://github.com/Grid2op/grid2op.git
clone_if_missing powergym https://github.com/siemens/powergym.git
clone_if_missing powergridworld https://github.com/NatLabRockies/PowerGridworld.git
clone_if_missing gym-anm https://github.com/robinhenry/gym-anm.git
clone_if_missing commonpower https://github.com/TUMcps/commonpower.git
