import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_harmony(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", "scripts/verify-harmony.mjs", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_task_001_scope_secret_and_model_lint():
    clean = run_harmony("--task", "001")
    assert clean.returncode == 0, clean.stdout + clean.stderr

    scope_probe = ROOT / "schema" / "_scope_probe.txt"
    scope_probe.write_text("probe\n", encoding="utf-8")
    try:
        blocked = run_harmony("--task", "001")
        output = blocked.stdout + blocked.stderr
        assert blocked.returncode != 0
        assert "out of scope" in output
    finally:
        scope_probe.unlink(missing_ok=True)

    secret_probe = ROOT / "packages" / "db" / "src" / "db" / "_secret_probe.py"
    planted = "GEMINI_" + "API_KEY = " + repr("a" * 16) + "\n"
    secret_probe.write_text(planted, encoding="utf-8")
    try:
        blocked = run_harmony("--task", "001")
        output = blocked.stdout + blocked.stderr
        assert blocked.returncode != 0
        assert "secret scan" in output
    finally:
        secret_probe.unlink(missing_ok=True)

    model_probe = ROOT / "packages" / "db" / "src" / "db" / "_model_probe.py"
    model_probe.write_text('MODEL = "gemini-omni-1.2-flash"\n', encoding="utf-8")
    try:
        blocked = run_harmony("--lint-model-ids")
        output = blocked.stdout + blocked.stderr
        assert blocked.returncode != 0
        assert "hardcoded model id" in output
    finally:
        model_probe.unlink(missing_ok=True)

    clean_again = run_harmony("--lint-model-ids")
    assert clean_again.returncode == 0, clean_again.stdout + clean_again.stderr


def test_part_fence_and_wave_dependency_refuse():
    part = run_harmony("--task", "042")
    assert part.returncode != 0
    assert "out of scope" in (part.stdout + part.stderr) or "Part 1" in (part.stdout + part.stderr)

    missing_tag = run_harmony("--wave", "W2-A")
    assert missing_tag.returncode != 0
    assert "p1-w1" in (missing_tag.stdout + missing_tag.stderr)

    unknown = run_harmony("--wave", "W9-Z")
    assert unknown.returncode != 0
    assert "unknown wave" in (unknown.stdout + unknown.stderr)
