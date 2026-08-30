#!/usr/bin/env python3
"""Check that everything describing the SDK fleet agrees with sdks.yml.

The fleet is described in three places that have no mechanical link between
them: this repository's README table, the dispatch matrix that decides which
repositories get notified, and the SDK repositories themselves. They drifted
repeatedly, and every time it was a person who noticed rather than CI: the
README claimed all seven SDKs were generated when one was not, then claimed one
was hand-written after it had been restored to generating, and the developer
portal documented a dispatch payload in a form whose bug had already been fixed.

sdks.yml is the source of truth. This script fails when anything disagrees with
it.

Local checks always run. Live repository checks need network access and a
GitHub token, and are skipped without one so the script stays usable offline.

Usage:
    python3 scripts/check_sdk_manifest.py            # local checks only
    python3 scripts/check_sdk_manifest.py --live     # also verify the repositories
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "sdks.yml"
README = REPO_ROOT / "README.md"
DISPATCH = REPO_ROOT / ".github" / "workflows" / "dispatch.yml"

MODEL_LABELS = {"generated": "Generated", "reference": "Generated as reference"}


class Failures(list):
    def add(self, check: str, detail: str) -> None:
        self.append((check, detail))


def load_manifest() -> list[dict]:
    import yaml

    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    sdks = data.get("sdks") or []
    if not sdks:
        raise SystemExit(f"error: {MANIFEST.name} declares no SDKs")
    for entry in sdks:
        for key in ("repo", "language", "ecosystem", "model", "generated_path"):
            if key not in entry:
                raise SystemExit(f"error: {entry.get('repo', '?')} is missing '{key}'")
        if entry["model"] not in MODEL_LABELS:
            raise SystemExit(
                f"error: {entry['repo']} has unknown model {entry['model']!r}; "
                f"expected one of {sorted(MODEL_LABELS)}"
            )
    return sdks


def check_dispatch_matrix(sdks: list[dict], failures: Failures) -> None:
    """Every SDK in the manifest must actually be notified, and vice versa."""
    text = DISPATCH.read_text(encoding="utf-8")
    listed = set(re.findall(r"^\s*-\s+(xyo-financial/sdk-[a-z0-9-]+)\s*$", text, re.M))
    declared = {s["repo"] for s in sdks}

    for repo in sorted(declared - listed):
        failures.add("dispatch", f"{repo} is in {MANIFEST.name} but not in the dispatch matrix, so it is never notified")
    for repo in sorted(listed - declared):
        failures.add("dispatch", f"{repo} is dispatched to but absent from {MANIFEST.name}")


def check_readme_table(sdks: list[dict], failures: Failures) -> None:
    """The README table must list every SDK with the model the manifest declares."""
    text = README.read_text(encoding="utf-8")

    for entry in sdks:
        repo = entry["repo"]
        row = next(
            (line for line in text.splitlines() if line.startswith("|") and f"`{repo}`" in line),
            None,
        )
        if row is None:
            failures.add("readme", f"{repo} has no row in the README table")
            continue
        expected = MODEL_LABELS[entry["model"]]
        if expected not in row:
            failures.add(
                "readme",
                f"{repo} is declared '{entry['model']}' but its README row does not say {expected!r}",
            )

    for repo in re.findall(r"`(xyo-financial/sdk-[a-z0-9-]+)`", text):
        if repo not in {s["repo"] for s in sdks}:
            failures.add("readme", f"{repo} appears in README.md but is absent from {MANIFEST.name}")


def gh_file(repo: str, path: str) -> str | None:
    """Fetch a file from a repository's default branch, or None if absent."""
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}", "--jq", ".content"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    import base64

    try:
        return base64.b64decode(result.stdout.strip()).decode("utf-8", "replace")
    except Exception:
        return None


def check_live_repositories(sdks: list[dict], failures: Failures) -> None:
    """Verify each repository actually behaves the way the manifest says."""
    for entry in sdks:
        repo, model = entry["repo"], entry["model"]
        workflow = gh_file(repo, ".github/workflows/generate.yml")

        if workflow is None:
            failures.add("live", f"{repo} has no .github/workflows/generate.yml, so a spec tag reaches nothing")
            continue
        if "spec_tagged" not in workflow:
            failures.add("live", f"{repo} does not subscribe to spec_tagged, so the dispatch is ignored")
        if "openapi-generator-cli" not in workflow:
            failures.add(
                "live",
                f"{repo} is declared '{model}' but its workflow never invokes the generator",
            )

        if model == "reference":
            # The isolation is what makes 'reference' true rather than a claim:
            # the generated tree must be kept out of release archives.
            attrs = gh_file(repo, ".gitattributes") or ""
            if f"{entry['generated_path']}/ export-ignore" not in attrs:
                failures.add(
                    "live",
                    f"{repo} is declared 'reference' but {entry['generated_path']}/ "
                    f"is not export-ignored, so it would ship in release archives",
                )


def main(argv: list[str]) -> int:
    live = "--live" in argv[1:]
    sdks = load_manifest()
    failures = Failures()

    print(f"Checking {len(sdks)} SDKs declared in {MANIFEST.name}\n")

    check_dispatch_matrix(sdks, failures)
    check_readme_table(sdks, failures)
    print("  [ok] dispatch matrix and README table read")

    if live:
        if not (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")):
            print("  [skip] live checks need GH_TOKEN or GITHUB_TOKEN")
        else:
            check_live_repositories(sdks, failures)
            print("  [ok] repositories inspected")
    else:
        print("  [skip] live repository checks (pass --live to enable)")

    if failures:
        print(f"\n{len(failures)} disagreement(s) with {MANIFEST.name}:", file=sys.stderr)
        for check, detail in failures:
            print(f"  [{check}] {detail}", file=sys.stderr)
        print(
            f"\nUpdate {MANIFEST.name} if the fleet genuinely changed, otherwise "
            "correct whatever has drifted away from it.",
            file=sys.stderr,
        )
        return 1

    print("\nEverything agrees with the manifest.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
