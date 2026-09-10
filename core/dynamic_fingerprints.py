# -*- coding: utf-8 -*-
"""
Dynamic Chapter Structure Fingerprints (8类动态章节结构指纹)
Replaces rigid 6-beat template with flexible, genre-adapted narrative topologies:
- ASSAULT (强攻破阵)
- INVESTIGATION (侦查解谜)
- CRISIS (绝境败退)
- ENSEMBLE (群像交织)
- PURSUIT (绝命追逃)
- TRIAL (公堂博弈)
- GOVERNANCE (治理推演)
- LIFESTYLE (市井凡尘)
Plus STANDARD_LONG for full backward compatibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ChapterFingerprintSpec:
    fingerprint_id: str
    name_zh: str
    description: str
    min_beats: int
    max_beats: int
    min_scenes: int
    required_roles: tuple[str, ...]
    allowed_roles: tuple[str, ...]


FINGERPRINT_SPECS: dict[str, ChapterFingerprintSpec] = {
    "STANDARD_LONG": ChapterFingerprintSpec(
        fingerprint_id="STANDARD_LONG",
        name_zh="标准长篇冲突型",
        description="经典商业网文高强度对峙与反转章型",
        min_beats=6,
        max_beats=8,
        min_scenes=2,
        required_roles=("ACTION", "COUNTERMOVE", "REPLAN", "REVELATION", "COST", "HOOK"),
        allowed_roles=("ACTION", "COUNTERMOVE", "REPLAN", "REVELATION", "COST", "HOOK", "CONVERGENCE", "EVALUATION"),
    ),
    "ASSAULT": ChapterFingerprintSpec(
        fingerprint_id="ASSAULT",
        name_zh="强攻破阵型",
        description="突袭、决战、刺杀、强行攻坚破阵",
        min_beats=4,
        max_beats=6,
        min_scenes=1,
        required_roles=("ACTION", "COUNTERMOVE", "BREAKTHROUGH", "HOOK"),
        allowed_roles=("ACTION", "COUNTERMOVE", "BREAKTHROUGH", "COST", "SACRIFICE", "HOOK", "CLIMAX"),
    ),
    "INVESTIGATION": ChapterFingerprintSpec(
        fingerprint_id="INVESTIGATION",
        name_zh="侦查解谜型",
        description="探案、剥洋葱、禁地探秘、解密上古阴谋",
        min_beats=4,
        max_beats=6,
        min_scenes=1,
        required_roles=("DISCOVERY", "OBSTACLE", "DEDUCTION", "HOOK"),
        allowed_roles=("DISCOVERY", "OBSTACLE", "DEDUCTION", "REVELATION", "DECISION", "HOOK"),
    ),
    "CRISIS": ChapterFingerprintSpec(
        fingerprint_id="CRISIS",
        name_zh="绝境败退型",
        description="反派设伏、阵线崩溃、断尾求生、战略转移",
        min_beats=4,
        max_beats=6,
        min_scenes=1,
        required_roles=("THREAT", "RETREAT", "SACRIFICE", "HOOK"),
        allowed_roles=("THREAT", "RETREAT", "DAMAGE_CONTROL", "SACRIFICE", "DESPAIR", "HOOK"),
    ),
    "ENSEMBLE": ChapterFingerprintSpec(
        fingerprint_id="ENSEMBLE",
        name_zh="群像交织型",
        description="多战场联动、双视角平行推进、会师碰头",
        min_beats=4,
        max_beats=7,
        min_scenes=2,
        required_roles=("PARALLEL_A", "PARALLEL_B", "COLLISION", "HOOK"),
        allowed_roles=("PARALLEL_A", "PARALLEL_B", "COLLISION", "AFTERMATH", "FRICTION", "HOOK"),
    ),
    "PURSUIT": ChapterFingerprintSpec(
        fingerprint_id="PURSUIT",
        name_zh="绝命追逃型",
        description="荒野逃亡、诱敌深入、反杀伏击、险象环生",
        min_beats=4,
        max_beats=6,
        min_scenes=1,
        required_roles=("AMBUSH", "PURSUIT", "TRAP", "HOOK"),
        allowed_roles=("AMBUSH", "PURSUIT", "TRAP", "ESCAPE", "COUNTER_KILL", "HOOK"),
    ),
    "TRIAL": ChapterFingerprintSpec(
        fingerprint_id="TRIAL",
        name_zh="公堂博弈型",
        description="法庭辩论、大殿权谋公审、朝堂逼宫、舆论交锋",
        min_beats=4,
        max_beats=6,
        min_scenes=1,
        required_roles=("CHARGE", "DEFENSE", "EVIDENCE", "HOOK"),
        allowed_roles=("CHARGE", "DEFENSE", "EVIDENCE", "CROSS_EXAM", "VERDICT", "HOOK"),
    ),
    "GOVERNANCE": ChapterFingerprintSpec(
        fingerprint_id="GOVERNANCE",
        name_zh="治理推演型",
        description="政令推行、利益妥协、二阶反噬、战后重建",
        min_beats=4,
        max_beats=6,
        min_scenes=1,
        required_roles=("POLICY", "BACKLASH", "COMPROMISE", "HOOK"),
        allowed_roles=("POLICY", "BACKLASH", "COMPROMISE", "TRADE_OFF", "INSTITUTION_BUILD", "HOOK"),
    ),
    "LIFESTYLE": ChapterFingerprintSpec(
        fingerprint_id="LIFESTYLE",
        name_zh="市井凡尘型",
        description="战后休整、烟火人情、情感升温、归隐听书",
        min_beats=3,
        max_beats=5,
        min_scenes=1,
        required_roles=("DAILY", "EMOTION", "HOOK"),
        allowed_roles=("DAILY", "MEMORY", "EMOTION", "EPIPHANY", "CONVERSATION", "HOOK"),
    ),
}


def validate_chapter_fingerprint(
    chapter_mode_or_payload: str | dict[str, Any],
    dynamic_beats: list[dict[str, Any]] | None = None,
    scenes: list[dict[str, Any]] | None = None
) -> list[str]:
    """
    Validates whether the dynamic beats and scenes of a chapter conform to
    its designated chapter mode / structure fingerprint.
    Accepts either a full chapter payload dictionary or positional args.
    Returns list of error messages.
    """
    if isinstance(chapter_mode_or_payload, dict):
        payload = chapter_mode_or_payload
        mode = str(payload.get("chapter_mode") or "STANDARD_LONG").upper().strip()
        beats = payload.get("dynamic_beats") or []
        sc = payload.get("scene_payloads") or payload.get("scenes") or []
    else:
        mode = str(chapter_mode_or_payload or "STANDARD_LONG").upper().strip()
        beats = dynamic_beats or []
        sc = scenes or []

    if mode not in FINGERPRINT_SPECS:
        mode = "STANDARD_LONG"

    spec = FINGERPRINT_SPECS[mode]
    errors = []

    beat_count = len(beats)
    if beat_count < spec.min_beats:
        errors.append(
            f"Mode {mode} beat shortfall: expected at least {spec.min_beats} beats, got {beat_count}"
        )
    elif beat_count > spec.max_beats:
        errors.append(
            f"Mode {mode} beat excess: expected at most {spec.max_beats} beats, got {beat_count}"
        )

    scene_count = len(sc)
    if scene_count < spec.min_scenes:
        errors.append(
            f"Mode {mode} scene shortfall: expected at least {spec.min_scenes} scenes, got {scene_count}"
        )

    # Check presence of required roles
    observed_roles = [b.get("role", "").upper().strip() for b in beats]
    for req in spec.required_roles:
        if req not in observed_roles:
            # Allow common aliases (e.g. BREAKTHROUGH ~ REPLAN, SACRIFICE ~ COST)
            alias_map = {
                "BREAKTHROUGH": {"REPLAN", "CLIMAX"},
                "SACRIFICE": {"COST"},
                "DEDUCTION": {"REPLAN", "REVELATION"},
                "COLLISION": {"COUNTERMOVE", "REPLAN"},
                "TRAP": {"COUNTERMOVE"},
                "DEFENSE": {"COUNTERMOVE"},
                "EVIDENCE": {"REVELATION"},
                "BACKLASH": {"COUNTERMOVE"},
                "COMPROMISE": {"REPLAN", "COST"},
                "EMOTION": {"REVELATION", "COST"},
            }
            aliases = alias_map.get(req, set())
            if not any(alias in observed_roles for alias in aliases):
                errors.append(f"Mode {mode} missing required beat role: '{req}'")

    return errors
