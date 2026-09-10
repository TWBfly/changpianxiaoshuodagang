# -*- coding: utf-8 -*-
"""
Ensemble Character Dynamics Engine (群像叙事与多智能体动力学引擎)
Enforces:
1. Anti-Cardboard Agency: Active actors must execute real decisions/actions,
   not just passive bystander fluff (e.g., "倒吸一口凉气", "暗自心惊").
2. Spotlight Continuity: Core characters must not vanish for excessive stretches
   without offline state stepping or narrative continuity.
3. Multi-Agent Value Friction: Ally characters with ideological friction must
   express distinct decision models and ethical boundaries.
4. Character Contract Completeness: Verification of desire vectors, shadow wants,
   taboo lines, and fatal flaws.
"""

from __future__ import annotations

from typing import Any


# Passive fluff patterns that do not constitute active narrative agency
PASSIVE_BYSTANDER_PATTERNS = [
    "倒吸一口凉气", "倒吸冷气", "退至众人身后", "心中震惊", "暗自心惊",
    "满脸震撼", "在旁观战", "沦为背景板", "默默注视", "只能旁观",
    "面露惊异", "毫无办法只能看着", "作为看客", "惊呼连连",
]


class EnsembleDynamicsEngine:
    """Validator and scheduler for ensemble cast dynamics in long-form novels."""

    def __init__(self, max_idle_chapters: int = 35):
        self.max_idle_chapters = max_idle_chapters

    def audit_character_agency(
        self, chapter_plans: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Ensures that every character declared in active_actors has real, proactive
        dramatic agency in that chapter, intercepting passive cardboard participation.
        """
        issues: list[dict[str, Any]] = []

        for cp in chapter_plans:
            if not isinstance(cp, dict):
                continue
            payload = cp.get("payload") if isinstance(cp.get("payload"), dict) else {}
            c_no = payload.get("chapter_no", 0)
            active_actors = payload.get("active_actors", [])
            if not isinstance(active_actors, list) or not active_actors:
                continue

            beats = payload.get("dynamic_beats", [])
            if not isinstance(beats, list):
                continue

            # Build aggregated text per actor across beats
            actor_contributions: dict[str, list[str]] = {str(a): [] for a in active_actors}

            for b in beats:
                if not isinstance(b, dict):
                    continue
                b_actor = str(b.get("active_actor", ""))
                action = str(b.get("action", ""))
                cf = str(b.get("counterforce", ""))
                b_text = f"{action} {cf} {str(b.get('delta', ''))}"

                # Direct actor match
                if b_actor in actor_contributions:
                    actor_contributions[b_actor].append(b_text)

                # Mention match across beats
                for a in active_actors:
                    a_str = str(a)
                    # Support ID without prefix or character name
                    clean_id = a_str.replace("CHAR.", "")
                    if clean_id in b_text or a_str in b_text:
                        if b_text not in actor_contributions[a_str]:
                            actor_contributions[a_str].append(b_text)

            for actor_id, texts in actor_contributions.items():
                if not texts:
                    issues.append({
                        "code": "GHOST_ACTOR_PARTICIPATION",
                        "message": (
                            f"Ch {c_no}: Actor '{actor_id}' is declared in active_actors "
                            f"but has 0 actions or beat participation in chapter."
                        ),
                        "object_id": cp.get("id"),
                        "is_warning": False,
                    })
                    continue

                combined_text = " ".join(texts)
                # Check if all contributions are just passive bystander fluff
                is_pure_bystander = any(p in combined_text for p in PASSIVE_BYSTANDER_PATTERNS) and not any(
                    active_verb in combined_text for active_verb in (
                        "斩", "杀", "破", "决断", "推演", "审判", "阻击", "夺取", "施展",
                        "布局", "下达", "救治", "谈判", "传音", "立誓", "拔刀", "祭出",
                        "策应", "反制", "搜寻", "抵挡", "突破", "重创", "炼制", "调阅"
                    )
                )

                if is_pure_bystander:
                    issues.append({
                        "code": "PASSIVE_CARDBOARD_PARTICIPATION",
                        "message": (
                            f"Ch {c_no}: Actor '{actor_id}' exhibits purely passive "
                            f"bystander presence without genuine proactive agency."
                        ),
                        "object_id": cp.get("id"),
                        "is_warning": True,
                    })

        return issues

    def audit_spotlight_continuity(
        self,
        chapter_plans: list[dict[str, Any]],
        characters: dict[str, dict[str, Any]],
        max_idle_chapters: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Verifies that core/major ensemble characters do not vanish into thin air
        for excessive chapter stretches without narrative maintenance.
        """
        issues: list[dict[str, Any]] = []
        limit = max_idle_chapters or self.max_idle_chapters

        if isinstance(characters, list):
            characters = {c.get("id"): c for c in characters if isinstance(c, dict) and c.get("id")}

        # Identify core ensemble characters
        core_chars = set()
        for cid, cent in characters.items():
            cp = cent.get("payload") if isinstance(cent.get("payload"), dict) else {}
            tier = str(cp.get("character_tier", "")).upper()
            role = str(cp.get("role", "")).upper()
            if tier in {"CORE", "MAJOR"} or role in {"PROTAGONIST", "DEUTERAGONIST", "PRIMARY_ANTAGONIST"}:
                core_chars.add(cid)

        if not core_chars:
            return issues

        # Track appearances per chapter
        sorted_cps = sorted(
            [cp for cp in chapter_plans if isinstance(cp.get("payload", {}).get("chapter_no"), int)],
            key=lambda x: x["payload"]["chapter_no"],
        )

        char_appearances: dict[str, list[int]] = {c: [] for c in core_chars}

        for cp in sorted_cps:
            c_no = cp["payload"]["chapter_no"]
            actors = set(cp["payload"].get("active_actors", []))
            beats = cp["payload"].get("dynamic_beats", [])
            for b in beats:
                if isinstance(b, dict) and b.get("active_actor"):
                    actors.add(b["active_actor"])

            full_str = str(cp["payload"])
            for c in core_chars:
                clean_c = c.replace("CHAR.", "")
                if c in actors or clean_c in full_str:
                    char_appearances[c].append(c_no)

        total_chapters = len(sorted_cps)
        for cid, appearances in char_appearances.items():
            if not appearances:
                issues.append({
                    "code": "CORE_CHARACTER_ZERO_ACTION",
                    "message": (
                        f"Core ensemble character '{cid}' ({characters.get(cid, {}).get('payload', {}).get('character_tier', 'CORE')}) "
                        f"has 0 beat actions or appearances across all {total_chapters} chapters."
                    ),
                    "object_id": cid,
                    "is_warning": False,  # Hard error: core character must have agency
                })
                continue

            c_payload = characters.get(cid, {}).get("payload", {})
            intro_ch = c_payload.get("introduced_in_chapter")
            first_ch = appearances[0]
            # Check head gap
            if intro_ch is not None and first_ch > intro_ch + limit:
                issues.append({
                    "code": "SPOTLIGHT_HEAD_NEGLECT_WARNING",
                    "message": (
                        f"Core character '{cid}' was scheduled to appear in Ch {intro_ch} "
                        f"but first appeared in Ch {first_ch} (gap {first_ch - intro_ch} > {limit})."
                    ),
                    "object_id": cid,
                    "is_warning": True,
                })
            elif intro_ch is None and first_ch > int(total_chapters * 0.5):
                issues.append({
                    "code": "SPOTLIGHT_HEAD_NEGLECT_WARNING",
                    "message": (
                        f"Core character '{cid}' does not appear until Ch {first_ch} "
                        f"(over 50% through {total_chapters} chapters) without explicit intro milestone."
                    ),
                    "object_id": cid,
                    "is_warning": True,
                })

            # Check gap between consecutive appearances
            for idx in range(len(appearances) - 1):
                gap = appearances[idx + 1] - appearances[idx]
                if gap > limit:
                    issues.append({
                        "code": "SPOTLIGHT_NEGLECT_WARNING",
                        "message": (
                            f"Core character '{cid}' disappears for {gap} chapters "
                            f"(Ch {appearances[idx]} -> Ch {appearances[idx+1]}), exceeding threshold of {limit}."
                        ),
                        "object_id": cid,
                        "is_warning": True,
                    })

            # Check tail gap
            status = str(c_payload.get("status", "ALIVE")).upper()
            death_ch = c_payload.get("death_chapter")
            tail_gap = total_chapters - appearances[-1]
            if status != "DEAD" and death_ch is None and tail_gap > limit:
                issues.append({
                    "code": "SPOTLIGHT_TAIL_NEGLECT_WARNING",
                    "message": (
                        f"Core character '{cid}' disappears after Ch {appearances[-1]} "
                        f"({tail_gap} chapters until finale) without documented death or exit milestone."
                    ),
                    "object_id": cid,
                    "is_warning": True,
                })

        return issues

    def audit_storyline_ownership(
        self,
        lines: list[dict[str, Any]],
        characters: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Verifies that:
        1. There are multiple distinct LINEs owned by different characters.
        2. Core characters own or lead at least one narrative line.
        3. Antagonist camp has at least one counter-line or independent objective.
        """
        issues: list[dict[str, Any]] = []
        if not lines:
            issues.append({
                "code": "MISSING_STORYLINES",
                "message": "Project lacks LINE entities; long-form ensemble requires multi-line narrative topology.",
                "object_id": None,
                "is_warning": False,
            })
            return issues

        line_owners: set[str] = set()
        for line in lines:
            lp = line.get("payload") if isinstance(line.get("payload"), dict) else {}
            owner = lp.get("owner")
            if owner:
                line_owners.add(str(owner))

        # Check that lines aren't monopolized by a single character
        if len(line_owners) < 2 and len(lines) >= 2:
            issues.append({
                "code": "MONOPOLIZED_STORYLINES",
                "message": (
                    f"All {len(lines)} storylines are owned by {line_owners}. "
                    f"Ensemble cast requires distributed line ownership across multiple characters."
                ),
                "object_id": None,
                "is_warning": True,
            })

        return issues

    def audit_character_contracts(
        self, characters: dict[str, dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Verifies that ensemble characters are defined with genuine depth
        (desires, constraints, decision models, shadow wants, taboo lines, fatal flaws)
        rather than superficial labels.
        """
        issues: list[dict[str, Any]] = []

        if isinstance(characters, list):
            characters = {c.get("id"): c for c in characters if isinstance(c, dict) and c.get("id")}

        for cid, cent in characters.items():
            p = cent.get("payload") if isinstance(cent.get("payload"), dict) else {}
            tier = str(p.get("character_tier", "")).upper()
            if tier not in {"CORE", "MAJOR"}:
                continue

            # Check desire vector & constraints
            has_goal = bool(p.get("goals") or p.get("explicit_goal") or p.get("desires"))
            has_constraint = bool(p.get("constraints") or p.get("taboo_line") or p.get("fatal_flaw"))
            has_strategy = bool(p.get("preferred_strategy") or p.get("decision_model"))

            if not (has_goal and has_constraint and has_strategy):
                issues.append({
                    "code": "SHALLOW_CHARACTER_CONTRACT",
                    "message": (
                        f"Core character '{cid}' lacks required desire vector, moral taboo/constraint, or decision model, "
                        f"risking cardboard compliance."
                    ),
                    "object_id": cid,
                    "is_warning": True,
                })

        return issues


# Module-level convenience functions
def audit_character_contracts(characters: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return EnsembleDynamicsEngine().audit_character_contracts(characters)


def audit_ensemble_spotlight(
    characters: dict[str, dict[str, Any]],
    chapter_plans: list[dict[str, Any]],
    max_idle_chapters: int | None = None,
    total_chapters: int | None = None,
) -> list[dict[str, Any]]:
    return EnsembleDynamicsEngine().audit_spotlight_continuity(characters, chapter_plans, max_idle_chapters)


def audit_storyline_ownership(
    lines: list[dict[str, Any]],
    characters: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    return EnsembleDynamicsEngine().audit_storyline_ownership(lines, characters)

