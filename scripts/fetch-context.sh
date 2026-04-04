#!/usr/bin/env bash
# Fetches context.md from each product's private GitHub repo and caches locally.
# Requires GITHUB_TOKEN env var with repo read access.
# Always exits 0 so it never blocks hooks.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "[fetch-context] GITHUB_TOKEN not set — skipping fetch"
  exit 0
fi

declare -A REPOS=(
  [sagokraft]="Sagokraft"
  [selftaped]="Selftaped"
  [fellingpal]="FellingPal"
)

for repo in "${!REPOS[@]}"; do
  folder="${REPOS[$repo]}"
  target_dir="${ROOT_DIR}/${folder}"
  target_file="${target_dir}/context.md"
  tmp_file="${target_file}.tmp"

  if curl -sf \
    -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github.raw+json" \
    "https://api.github.com/repos/jesperhagg/${repo}/contents/context.md" \
    -o "${tmp_file}" 2>/dev/null; then
    mv "${tmp_file}" "${target_file}"
    echo "[fetch-context] ${folder}: updated"
  else
    rm -f "${tmp_file}"
    if [ -f "${target_file}" ]; then
      echo "[fetch-context] ${folder}: fetch failed (using cached)"
    else
      echo "[fetch-context] ${folder}: not found in remote repo"
    fi
  fi
done
