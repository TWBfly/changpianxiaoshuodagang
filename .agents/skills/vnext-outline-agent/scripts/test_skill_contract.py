from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def test_skill_contract():
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: vnext-outline-agent" in skill
    assert "Neo4j" in skill
    assert "DEGRADED" in skill
    assert (SKILL_ROOT / "references" / "runtime-core.md").exists()
    assert (SKILL_ROOT / "references" / "output-contract.md").exists()


if __name__ == "__main__":
    test_skill_contract()
    print("skill contract ok")
