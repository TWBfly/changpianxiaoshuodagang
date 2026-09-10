# -*- coding: utf-8 -*-
"""
Narrative Physics Validator (叙事物理学与因果校验引擎)
Enforces:
1. Spatiotemporal Continuity & Anti-Teleportation (时空连续性与位移航速物理律)
2. Entity Chain of Custody & Physical Conservation (道具保管链与实体守恒律)
3. Epistemic Asymmetry & Real Counterforce (信息差与真实反制阻抗校验)
4. Anti-Actor Forgery (严禁动作文本与主动者标签脱节的伪造行为)
"""

from __future__ import annotations

from typing import Any
from genres.base_driver import BaseGenreDriver, get_genre_driver
from genres.xianxia import XianxiaGenreDriver
from tones.base_tone import BaseToneDriver, get_tone_driver
from tones.shuangwen import ShuangwenToneDriver
from core.ensemble_engine import EnsembleDynamicsEngine


# Fluff phrases that cannot serve as valid counterforce on their own
BANNED_COUNTERFORCE_FLUFF = [
    "展现横推一切", "展现至尊神威", "全书大圆满", "展现核心戏剧推动力",
    "胜利由烈士鲜血铸就", "全歼敌人并大获全胜", "展现无敌手段", "敌人尽数俯首称臣",
    "全书最高思想主题升华", "展现无可匹敌之威",
]


class NarrativePhysicsValidator:
    def __init__(
        self,
        genre_driver: BaseGenreDriver | None = None,
        tone_driver: BaseToneDriver | None = None,
        ensemble_engine: EnsembleDynamicsEngine | None = None,
    ):
        self.genre = genre_driver or XianxiaGenreDriver()
        self.tone = tone_driver or ShuangwenToneDriver()
        self.ensemble = ensemble_engine or EnsembleDynamicsEngine()

    def audit_spatiotemporal_continuity(
        self,
        chapter_plans: list[dict[str, Any]],
        locations: dict[str, dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Validates that chapters progress logically across time and space.
        Catches time reversions and unexplainable teleportation across vast distances.
        """
        issues = []
        locations = locations or {}

        prev_day = None
        prev_loc = None
        prev_realm = None
        prev_ch_no = None

        sorted_plans = sorted(
            [
                cp for cp in chapter_plans
                if isinstance(cp, dict)
                and isinstance(cp.get("payload"), dict)
                and isinstance(cp["payload"].get("chapter_no"), int)
            ],
            key=lambda x: x["payload"]["chapter_no"],
        )

        for cp in sorted_plans:
            p = cp["payload"]
            c_no = p["chapter_no"]
            st = p.get("spacetime") or {}
            
            day = st.get("story_day")
            loc = st.get("location_id") or p.get("location")
            realm = st.get("realm_id") or "MAIN"

            # 1. Temporal monotonicity
            if day is not None:
                if prev_day is not None and day < prev_day:
                    issues.append({
                        "code": "TEMPORAL_REGRESSION",
                        "message": f"Time reversed from Day {prev_day} in Ch {prev_ch_no} to Day {day} in Ch {c_no}",
                        "object_id": cp.get("id"),
                    })

            # 2. Spatial continuity
            if loc and prev_loc and loc != prev_loc and day is not None and prev_day is not None:
                elapsed_days = max(day - prev_day, 0.1)
                # Calculate or lookup distance between locations
                loc_a = locations.get(prev_loc, {}).get("payload", {})
                loc_b = locations.get(loc, {}).get("payload", {})
                
                # Check realm jump
                if realm != prev_realm:
                    # Realm shift requires realm-shift travel mode or portal
                    travel_mode = st.get("travel_mode", "WALK")
                    if travel_mode not in {"TELEPORT", "REALM_PORTAL", "GHOST_REALM_SHIFT", "DALUO_TEAR_VOID", "SPACE_WARP"}:
                        issues.append({
                            "code": "UNAUTHORIZED_REALM_JUMP",
                            "message": f"Cross-realm shift from {prev_realm} to {realm} in Ch {c_no} without realm portal.",
                            "object_id": cp.get("id"),
                        })
                else:
                    # Same realm distance check
                    dist = float(st.get("distance_traveled", 0.0))
                    if dist > 0:
                        travel_mode = st.get("travel_mode", "WALK")
                        max_daily = self.genre.travel_speed_limits.get(travel_mode, 100.0)
                        max_possible = max_daily * elapsed_days
                        if dist > max_possible * 1.5:  # 1.5x tolerance
                            issues.append({
                                "code": "SPATIOTEMPORAL_TELEPORTATION_VIOLATION",
                                "message": f"Distance {dist}li traveled exceeds maximum physical capacity {max_possible:.1f}li in {elapsed_days:.1f} days ({travel_mode}).",
                                "object_id": cp.get("id"),
                            })

            if day is not None:
                prev_day = day
            if loc:
                prev_loc = loc
            if realm:
                prev_realm = realm
            prev_ch_no = c_no

        return issues

    def audit_chain_of_custody(
        self,
        chapter_plans: list[dict[str, Any]],
        props: dict[str, dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Validates the physical conservation of props, treasures, and evidence.
        Ensures items are not used before introduced, nor used after destruction.
        """
        issues = []
        props = props or {}

        # Track item state across story: item_id -> {"status": ..., "holder": ..., "intro_ch": ...}
        item_ledger: dict[str, dict[str, Any]] = {}
        for p_id, p_ent in props.items():
            payload = p_ent.get("payload", {})
            item_ledger[p_id] = {
                "status": payload.get("status", "ACTIVE"),
                "holder": payload.get("owner"),
                "intro_ch": payload.get("introduced_in_chapter", 1),
            }

        sorted_plans = sorted(
            [
                cp for cp in chapter_plans
                if isinstance(cp, dict)
                and isinstance(cp.get("payload"), dict)
                and isinstance(cp["payload"].get("chapter_no"), int)
            ],
            key=lambda x: x["payload"]["chapter_no"],
        )

        for cp in sorted_plans:
            p = cp["payload"]
            c_no = p["chapter_no"]
            items_used = list(p.get("items_used") or [])
            
            # Scan beats for item mentions
            for b in p.get("dynamic_beats", []) if isinstance(p.get("dynamic_beats"), list) else []:
                if isinstance(b, dict) and b.get("item_ref"):
                    items_used.append(b["item_ref"])

            for item_id in set(items_used):
                if item_id in item_ledger:
                    state = item_ledger[item_id]
                    # Check introduction chapter
                    if c_no < state["intro_ch"]:
                        issues.append({
                            "code": "CHAIN_OF_CUSTODY_VIOLATION",
                            "message": f"Item {item_id} used in Ch {c_no} before introduced at Ch {state['intro_ch']}.",
                            "object_id": cp.get("id"),
                        })
                    # Check destruction status
                    if state["status"] in {"DESTROYED", "CONSUMED", "SACRIFICED"}:
                        issues.append({
                            "code": "CHAIN_OF_CUSTODY_VIOLATION",
                            "message": f"Item {item_id} used in Ch {c_no} after being marked as {state['status']}.",
                            "object_id": cp.get("id"),
                        })

            # Check status transitions in this chapter
            item_changes = p.get("item_events", [])
            for ev in item_changes:
                iid = ev.get("item_id")
                action = ev.get("action")  # "ACQUIRE", "TRANSFER", "DESTROY", "CONSUME"
                new_holder = ev.get("new_holder")
                if iid in item_ledger:
                    if action in {"DESTROY", "CONSUME"}:
                        item_ledger[iid]["status"] = "DESTROYED"
                    elif action in {"ACQUIRE", "TRANSFER"} and new_holder:
                        item_ledger[iid]["holder"] = new_holder

        return issues

    # Alias for API consistency
    audit_item_chain_of_custody = audit_chain_of_custody

    def audit_counterforce_and_actor_authenticity(
        self,
        chapter_plans: list[dict[str, Any]],
        characters: dict[str, dict[str, Any]] | None = None,
        strict_counterforce: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Validates that counterforces are genuine obstacles rather than fluff praise,
        and that active_actor declared in beat metadata actually matches the action.
        """
        issues = []
        characters = characters or {}

        for cp in chapter_plans:
            if not isinstance(cp, dict) or not isinstance(cp.get("payload"), dict):
                continue
            p = cp["payload"]
            c_no = p.get("chapter_no", 0)
            
            # 1. Conflict Contract Check
            cc = p.get("conflict_contract") if isinstance(p.get("conflict_contract"), dict) else {}
            actor_a = p.get("actor_a") or cc.get("actor_a")
            actor_b = p.get("actor_b") or cc.get("actor_b")

            if actor_a and actor_b and actor_a == actor_b:
                issues.append({
                    "code": "SELF_CONFLICT_INVALID",
                    "message": f"Ch {c_no}: actor_a and actor_b cannot be identical ({actor_a})",
                    "object_id": cp.get("id"),
                    "is_warning": False,
                })

            # 2. Beat Counterforce Quality & Anti-Fluff
            beats = p.get("dynamic_beats", [])
            if not isinstance(beats, list):
                continue
            for idx, b in enumerate(beats):
                if not isinstance(b, dict):
                    continue
                b_id = b.get("beat_id") or f"CH{c_no}.B{idx+1}"
                cnt = b.get("counterforce", "")
                
                # Check for empty counterforce
                if not cnt or not cnt.strip():
                    issues.append({
                        "code": "EMPTY_COUNTERFORCE",
                        "message": f"Ch {c_no} Beat {b_id}: Counterforce is empty.",
                        "object_id": cp.get("id"),
                        "is_warning": False,
                    })
                    continue

                # Check for pure fluff phrases
                for fluff in BANNED_COUNTERFORCE_FLUFF:
                    if fluff in cnt and len(cnt.strip()) <= len(fluff) + 5:
                        code = "FLUFF_COUNTERFORCE_REJECTED" if strict_counterforce else "FLUFF_COUNTERFORCE_WARNING"
                        issues.append({
                            "code": code,
                            "message": f"Ch {c_no} Beat {b_id}: Counterforce is pure self-praising fluff ('{cnt}').",
                            "object_id": cp.get("id"),
                            "is_warning": not strict_counterforce,
                        })
                        break

                # 3. Anti-Actor Forgery: Action must involve active_actor
                active_actor = b.get("active_actor")
                action_text = b.get("action", "")
                if active_actor and active_actor in characters:
                    char_name = characters[active_actor].get("name", "")
                    # If actor is core/major, verify presence in action or cause
                    if char_name and len(char_name) >= 2:
                        full_context = f"{action_text} {b.get('cause_from_previous', '')} {b.get('actor_goal_before', '')}"
                        # Allow common titles or aliases if specified
                        aliases = characters[active_actor].get("payload", {}).get("aliases", [])
                        matches = [char_name, active_actor] + list(aliases)
                        if "(" in char_name:
                            matches.append(char_name.split("(")[0].strip())
                        if "（" in char_name:
                            matches.append(char_name.split("（")[0].strip())
                        if active_actor == "CHAR.gu_jinglan":
                            matches.extend(["少帅", "惊澜", "主角"])
                        
                        if not any(m in full_context for m in matches):
                            code = "ACTOR_FORGERY_LABEL_MISMATCH" if strict_counterforce else "ACTOR_LABEL_SUSPECT"
                            issues.append({
                                "code": code,
                                "message": f"Ch {c_no} Beat {b_id}: active_actor '{active_actor}' ({char_name}) not mentioned in beat action.",
                                "object_id": cp.get("id"),
                                "is_warning": not strict_counterforce,
                            })

        return issues

    @classmethod
    def audit_packet(
        cls,
        packet: dict[str, Any],
        strict_teleportation: bool = True,
        strict_item_custody: bool = True,
        strict_counterforce: bool = False,
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Runs comprehensive narrative physics audit on an outline packet:
        1. Spatiotemporal continuity & anti-teleportation
        2. Item chain of custody & physical conservation
        3. Counterforce quality & anti-actor forgery
        4. Genre worldview physics adherence
        """
        raw_entities = packet.get("entities", []) if isinstance(packet, dict) else []
        entities = [e for e in raw_entities if isinstance(e, dict) and e.get("id")]
        
        # Check root or project entity for genre & tone
        genre_str = packet.get("genre") if isinstance(packet, dict) else None
        tone_str = packet.get("tone") if isinstance(packet, dict) else None
        for e in entities:
            if str(e.get("kind", "")).upper() == "PROJECT":
                p_payload = e.get("payload", {})
                if isinstance(p_payload, dict):
                    if not genre_str:
                        genre_str = p_payload.get("genre")
                    if not tone_str:
                        tone_str = p_payload.get("tone")
                break

        try:
            genre_driver = get_genre_driver(genre_str or "XIANXIA")
        except Exception:
            genre_driver = XianxiaGenreDriver()

        try:
            tone_driver = get_tone_driver(tone_str) if tone_str else None
        except Exception:
            tone_driver = None

        validator = cls(genre_driver=genre_driver, tone_driver=tone_driver)

        chapter_plans = [e for e in entities if str(e.get("kind", "")).upper() == "CHAPTER_PLAN"]
        locations = {e["id"]: e for e in entities if str(e.get("kind", "")).upper() == "LOCATION"}
        props = {e["id"]: e for e in entities if str(e.get("kind", "")).upper() == "PROP"}
        characters = {e["id"]: e for e in entities if str(e.get("kind", "")).upper() in {"CHARACTER", "CHAR"}}

        errors = []
        warnings = []

        # 1. Spatiotemporal continuity
        st_issues = validator.audit_spatiotemporal_continuity(chapter_plans, locations)
        for issue in st_issues:
            if strict_teleportation:
                errors.append(issue)
            else:
                warnings.append(issue)

        # 2. Item Chain of Custody
        item_issues = validator.audit_item_chain_of_custody(chapter_plans, props)
        for issue in item_issues:
            if strict_item_custody:
                errors.append(issue)
            else:
                warnings.append(issue)

        # 3. Counterforce & Actor Authenticity
        cf_issues = validator.audit_counterforce_and_actor_authenticity(
            chapter_plans, characters, strict_counterforce=strict_counterforce
        )
        for issue in cf_issues:
            if issue.get("is_warning", False):
                warnings.append(issue)
            else:
                errors.append(issue)

        # 4. Genre mechanics audit
        for cp in chapter_plans:
            if not isinstance(cp, dict) or not isinstance(cp.get("payload"), dict):
                continue
            p = cp["payload"]
            c_no = p.get("chapter_no", 0)
            g_issues = genre_driver.validate_chapter_mechanics(p)
            for g_iss in g_issues:
                errors.append({
                    "code": "GENRE_PHYSICS_VIOLATION",
                    "message": g_iss,
                    "object_id": cp.get("id"),
                })

        # 5. Tone dynamics audit
        if tone_driver:
            for cp in chapter_plans:
                if not isinstance(cp, dict) or not isinstance(cp.get("payload"), dict):
                    continue
                p = cp["payload"]
                t_issues = tone_driver.validate_chapter_tone(p)
                for t_iss in t_issues:
                    errors.append({
                        "code": "TONE_VIOLATION",
                        "message": t_iss,
                        "object_id": cp.get("id"),
                    })

        # 6. Ensemble Character Dynamics audit
        agency_issues = validator.ensemble.audit_character_agency(chapter_plans)
        for issue in agency_issues:
            if issue.get("is_warning", False):
                warnings.append(issue)
            else:
                errors.append(issue)

        spotlight_issues = validator.ensemble.audit_spotlight_continuity(chapter_plans, characters)
        for issue in spotlight_issues:
            if issue.get("is_warning", True):
                warnings.append(issue)
            else:
                errors.append(issue)

        contract_issues = validator.ensemble.audit_character_contracts(characters)
        for issue in contract_issues:
            if issue.get("is_warning", True):
                warnings.append(issue)
            else:
                errors.append(issue)

        lines = [e for e in entities if str(e.get("kind", "")).upper() == "LINE"]
        if lines:
            line_issues = validator.ensemble.audit_storyline_ownership(lines, characters)
            for issue in line_issues:
                if issue.get("is_warning", True):
                    warnings.append(issue)
                else:
                    errors.append(issue)

        return {"errors": errors, "warnings": warnings}

