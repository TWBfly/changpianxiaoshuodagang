"""Deterministic Canon and graph-runtime primitives for the VNext outline Skill."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from urllib.parse import urlparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


class ValidationError(ValueError):
    def __init__(self, message: str, code: str = "VALIDATION_ERROR", object_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.object_id = object_id


@dataclass(frozen=True)
class CommitResult:
    project_id: str
    version: int
    snapshot_hash: str
    outbox_count: int


@dataclass
class ProjectionResult:
    applied: int
    degraded: list[dict]


@dataclass
class AuditReport:
    errors: list[dict]
    warnings: list[dict]
    counts: dict | None = None

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict:
        counts = self.counts or {"errors": len(self.errors), "warnings": len(self.warnings)}
        return {"ok": self.ok, "errors": self.errors, "warnings": self.warnings, "counts": counts}


def _append_graph_health(report: AuditReport, pending: list[dict], project_id: str) -> None:
    if not pending:
        return
    degraded = [row for row in pending if row.get("projection_status") == "DEGRADED"]
    if degraded:
        detail = degraded[0].get("projection_error") or "graph projection is degraded"
        report.warnings.append(_issue("GRAPH_DEGRADED", detail, project_id))
    else:
        report.warnings.append(_issue("GRAPH_PENDING", "graph projection has unapplied outbox changes", project_id))
    if report.counts is not None:
        report.counts["warnings"] = len(report.warnings)


PLACEHOLDER_NAMES = (
    "路人甲", "路人乙", "官员A", "官员B", "护卫一", "护卫二", "商人A",
    "弟子一", "弟子二", "村民一", "村民二", "神秘人", "某个手下", "一个神秘人",
)
REQUIRED_CHARACTER_FIELDS = (
    "identity", "desires", "goals", "interests", "constraints", "preferred_strategy",
)
REQUIRED_LIFE_PROFILE_FIELDS = (
    "biography", "decision_model", "private_life", "life_constraints", "knowledge_state", "misjudgments", "arc", "fate", "highlights",
)
PROVENANCE_KINDS = {
    "CHAR", "CHARACTER", "PERSON", "COHORT", "FACTION", "LOCATION", "RESOURCE",
    "OBJECT", "PROP", "EVIDENCE", "RULE", "EVENT", "LINE", "PROMISE", "CLIMAX",
    "ACT", "VOLUME", "TIMEPOINT", "CHAPTER_PLAN", "BEAT", "HUMAN_STATE",
}
CAUSAL_EDGE_TYPES = {"CAUSES", "PRECEDES", "RESULTS_IN"}
PACKET_MODES = {"SNAPSHOT", "PATCH"}
CHAPTER_MODES = {"STANDARD_LONG", "MAJOR_LONG", "QUIET_LONG"}
ALLOWED_NAMESPACES = {"CONTRACT", "CANON", "PLAN"}
ALLOWED_STATUSES = {
    "ACTIVE", "PROPOSED", "SUPERSEDED", "INVALIDATED", "QUARANTINED",
    "CLOSED", "RESOLVED", "PAID_OFF", "HEATING", "COLLIDING",
    "CLIMAX_READY", "CLOSING", "RESIDUE_ONLY", "DRAFT", "APPROVED",
}
CHAPTER_STAGEABILITY = {
    "STAGEABLE_CORE", "SUPPORTING_STAGEABLE", "SUMMARY_ONLY", "RESULT_ONLY", "LEDGER_ONLY",
}
CHAPTER_PLAN_REQUIRED_FIELDS = (
    "chapter_no", "volume_ref", "target_prose_contract", "chapter_function", "core_delta",
    "conflict_contract", "dynamic_beats", "payload_clusters", "scene_payloads",
    "explicit_compression", "continuation_source", "forbidden_drift",
)
VOLUME_REQUIRED_FIELDS = (
    "chapter_start", "chapter_end", "detailed_plot", "central_conflict",
    "turning_points", "payoff", "next_hook",
)
STAGEABLE_BEAT_REQUIRED_FIELDS = (
    "cause_from_previous", "active_actor", "action", "counterforce",
    "new_information_or_choice", "delta", "actor_goal_before", "actor_goal_after",
    "next_pressure_created",
)
CLUSTER_REQUIRED_FIELDS = (
    "cluster_id", "local_goal", "active_actors", "conflict_medium", "stageable_beats",
    "local_turn", "local_cost", "exit_state", "pressure_handed_to_next_cluster",
)
SCENE_REQUIRED_FIELDS = (
    "scene_id", "entry_state", "active_actor_goal", "opposing_goal_or_process",
    "immediate_stakes", "live_actions", "turn_or_reprice", "exit_state",
    "delta_dimensions", "payload_cluster_refs",
)


def _issue(code: str, message: str, object_id: str | None = None) -> dict:
    return {"code": code, "message": message, "object_id": object_id}


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def _is_final_full_book(packet: dict) -> bool:
    precision = packet.get("precision") if isinstance(packet, dict) else {}
    return isinstance(precision, dict) and str(precision.get("production_stage", "")).upper() == "FINAL_FULL_BOOK"


def audit_outline_scope(packet: dict) -> list[dict]:
    """Audit the hierarchy that makes a packet a complete long-form outline."""
    if not _is_final_full_book(packet):
        return []
    precision = packet.get("precision", {})
    if precision.get("full_book_detailed_required") is not True:
        return [_issue("FULL_BOOK_MODE_REQUIRED", "FINAL_FULL_BOOK requires full_book_detailed_required=true")]

    entities = packet.get("entities", []) if isinstance(packet, dict) else []
    valid_entities = [item for item in entities if isinstance(item, dict)]
    projects = [item for item in valid_entities if str(item.get("kind", "")).upper() == "PROJECT"]
    volumes = [item for item in valid_entities if str(item.get("kind", "")).upper() == "VOLUME"]
    plans = [item for item in valid_entities if str(item.get("kind", "")).upper() == "CHAPTER_PLAN"]
    errors: list[dict] = []

    if not projects:
        errors.append(_issue("PROJECT_ENTITY_MISSING", "FINAL_FULL_BOOK requires one PROJECT entity"))
    elif len(projects) > 1:
        errors.append(_issue("PROJECT_ENTITY_COUNT_INVALID", "FINAL_FULL_BOOK requires exactly one PROJECT entity"))
    else:
        project_payload = projects[0].get("payload") if isinstance(projects[0].get("payload"), dict) else {}
        synopsis = project_payload.get("one_sentence_synopsis")
        causal_summary = project_payload.get("causal_summary")
        if not isinstance(synopsis, str) or not synopsis.strip():
            code = "PROJECT_SYNOPSIS_MISSING" if not _present(synopsis) else "PROJECT_SYNOPSIS_INVALID"
            errors.append(_issue(code, "PROJECT needs a non-empty string one_sentence_synopsis", projects[0].get("id")))
        if not isinstance(causal_summary, str) or not causal_summary.strip():
            code = "PROJECT_CAUSAL_SUMMARY_MISSING" if not _present(causal_summary) else "PROJECT_CAUSAL_SUMMARY_INVALID"
            errors.append(_issue(code, "PROJECT needs a non-empty string causal_summary", projects[0].get("id")))

    expected_volumes = precision.get("expected_volumes")
    expected_chapters = precision.get("expected_chapters")
    if not isinstance(expected_volumes, int) or expected_volumes < 1 or not isinstance(expected_chapters, int) or expected_chapters < 1:
        errors.append(_issue("OUTLINE_SCOPE_MISSING", "FINAL_FULL_BOOK needs positive expected_volumes and expected_chapters"))
        return errors

    if len(volumes) != expected_volumes:
        errors.append(_issue("VOLUME_PLAN_MISSING", f"expected {expected_volumes} volumes, found {len(volumes)}"))

    ranges: list[tuple[int, int, str]] = []
    for volume in volumes:
        payload = volume.get("payload") if isinstance(volume.get("payload"), dict) else {}
        missing = [field for field in VOLUME_REQUIRED_FIELDS if not _present(payload.get(field))]
        if missing:
            errors.append(_issue("VOLUME_DETAIL_MISSING", f"volume needs: {', '.join(missing)}", volume.get("id")))
            continue
        start, end = payload.get("chapter_start"), payload.get("chapter_end")
        if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start or end > expected_chapters:
            errors.append(_issue("VOLUME_RANGE_INVALID", "volume chapter range is invalid", volume.get("id")))
            continue
        ranges.append((start, end, volume.get("id", "")))

    covered: list[int] = []
    for start, end, _ in sorted(ranges):
        covered.extend(range(start, end + 1))
    if covered != list(range(1, expected_chapters + 1)):
        errors.append(_issue("CHAPTER_COUNT_MISMATCH", "volume ranges must cover each chapter from 1 through expected_chapters exactly once"))

    volume_by_id = {volume.get("id"): (volume.get("payload") or {}) for volume in volumes}
    character_ids = {
        entity.get("id") for entity in valid_entities
        if str(entity.get("kind", "")).upper() in {"CHAR", "CHARACTER", "PERSON"} and isinstance(entity.get("id"), str)
    }
    seen_patterns: dict[tuple[str, str], str] = {}
    for plan in plans:
        payload = plan.get("payload") if isinstance(plan.get("payload"), dict) else {}
        number = payload.get("chapter_no")
        volume_id = payload.get("volume_ref")
        volume_payload = volume_by_id.get(volume_id)
        if volume_id not in volume_by_id:
            errors.append(_issue("CHAPTER_VOLUME_REFERENCE_INVALID", "chapter volume_ref must reference an existing VOLUME", plan.get("id")))
        elif isinstance(number, int) and isinstance(volume_payload, dict):
            start, end = volume_payload.get("chapter_start"), volume_payload.get("chapter_end")
            if not isinstance(start, int) or not isinstance(end, int) or not start <= number <= end:
                errors.append(_issue("CHAPTER_VOLUME_MISMATCH", f"chapter {number} is outside its volume range", plan.get("id")))
        actor_refs = []
        conflict = payload.get("conflict_contract") if isinstance(payload.get("conflict_contract"), dict) else {}
        actor_refs.extend(conflict.get(field) for field in ("actor_a", "actor_b"))
        actor_refs.extend(
            beat.get("active_actor")
            for beat in payload.get("dynamic_beats", [])
            if isinstance(beat, dict)
        )
        for actor in actor_refs:
            if isinstance(actor, str) and actor.startswith(("CHAR.", "PERSON.")) and actor not in character_ids:
                errors.append(_issue("CHAPTER_ACTOR_REFERENCE_INVALID", "chapter actor must reference a named character entity", plan.get("id")))
                break
        pattern = (str(payload.get("chapter_function", "")), str(payload.get("core_delta", "")))
        if all(pattern) and pattern in seen_patterns:
            errors.append(_issue("DUPLICATE_CHAPTER_BEAT_PATTERN", f"chapter repeats the function/core delta of {seen_patterns[pattern]}", plan.get("id")))
        elif all(pattern):
            seen_patterns[pattern] = plan.get("id", "")
    return errors


def audit_chapter_capacity(entity: dict, strict: bool = False) -> dict:
    """Compute chapter capacity from structured dramatic facts, never self-certification flags."""
    payload = entity.get("payload") if isinstance(entity, dict) else None
    failures: list[str] = []
    if not isinstance(payload, dict):
        return {
            "chapter_id": entity.get("id") if isinstance(entity, dict) else None,
            "target_prose_range": None,
            "stageable_core_beats": 0,
            "supporting_stageable_beats": 0,
            "summary_result_beats_removed": 0,
            "payload_clusters": 0,
            "core_scenes": 0,
            "mid_chapter_load": "FAIL",
            "writer_core_plot_invention_required": True,
            "final_capacity": "THIN",
            "failure_reasons": ["CHAPTER_PAYLOAD_INVALID"],
        }

    contract = payload.get("target_prose_contract")
    target_range = None
    mode = str((contract or {}).get("chapter_mode", "STANDARD_LONG")).upper() if isinstance(contract, dict) else "STANDARD_LONG"
    if mode not in CHAPTER_MODES:
        failures.append("INVALID_CHAPTER_MODE")
        mode = "STANDARD_LONG"
    if not isinstance(contract, dict):
        failures.append("TARGET_PROSE_CONTRACT_MISSING")
    else:
        target_min = contract.get("target_min")
        target_max = contract.get("target_max")
        if strict:
            target_default = contract.get("target_default")
            valid_policy_range = (
                isinstance(target_min, int) and not isinstance(target_min, bool)
                and isinstance(target_default, int) and not isinstance(target_default, bool)
                and isinstance(target_max, int) and not isinstance(target_max, bool)
                and 4000 <= target_min <= target_default <= target_max <= 6000
            )
            if not valid_policy_range:
                failures.append("TARGET_PROSE_RANGE_OUT_OF_POLICY")
            else:
                target_range = [target_min, target_max]
        elif not isinstance(target_min, (int, float)) or not isinstance(target_max, (int, float)) or target_min <= 0 or target_max < target_min:
            failures.append("TARGET_PROSE_CONTRACT_INVALID")
        else:
            target_range = [target_min, target_max]

    beats = payload.get("dynamic_beats")
    clusters = payload.get("payload_clusters")
    scenes = payload.get("scene_payloads")
    if not isinstance(beats, list):
        beats = []
        failures.append("DYNAMIC_BEATS_MISSING")
    if not isinstance(clusters, list):
        clusters = []
        failures.append("PAYLOAD_CLUSTERS_MISSING")
    if not isinstance(scenes, list):
        scenes = []
        failures.append("SCENE_PAYLOADS_MISSING")

    stageable = []
    removed = 0
    beat_ids: set[str] = set()
    for index, beat in enumerate(beats):
        if not isinstance(beat, dict):
            failures.append(f"BEAT_{index + 1}_INVALID")
            continue
        beat_id = beat.get("beat_id")
        if isinstance(beat_id, str):
            if beat_id in beat_ids:
                failures.append("DUPLICATE_BEAT_ID")
            beat_ids.add(beat_id)
        stageability = str(beat.get("stageability", "")).upper()
        if stageability not in CHAPTER_STAGEABILITY:
            failures.append(f"BEAT_{index + 1}_STAGEABILITY_INVALID")
            continue
        if stageability in {"SUMMARY_ONLY", "RESULT_ONLY", "LEDGER_ONLY"}:
            removed += 1
            continue
        missing = [field for field in STAGEABLE_BEAT_REQUIRED_FIELDS if not _present(beat.get(field))]
        if missing:
            failures.append(f"BEAT_{index + 1}_FIELDS_MISSING:{','.join(missing)}")
        stageable.append(beat)

    core_beats = [beat for beat in stageable if str(beat.get("stageability", "")).upper() == "STAGEABLE_CORE"]
    supporting_beats = [beat for beat in stageable if str(beat.get("stageability", "")).upper() == "SUPPORTING_STAGEABLE"]

    cluster_ids: set[str] = set()
    cluster_beat_refs: set[str] = set()
    for index, cluster in enumerate(clusters):
        if not isinstance(cluster, dict):
            failures.append(f"CLUSTER_{index + 1}_INVALID")
            continue
        missing = [field for field in CLUSTER_REQUIRED_FIELDS if not _present(cluster.get(field))]
        if missing:
            failures.append(f"CLUSTER_{index + 1}_FIELDS_MISSING:{','.join(missing)}")
        cluster_id = cluster.get("cluster_id")
        if isinstance(cluster_id, str):
            if cluster_id in cluster_ids:
                failures.append("DUPLICATE_CLUSTER_ID")
            cluster_ids.add(cluster_id)
        refs = cluster.get("stageable_beats")
        if isinstance(refs, list):
            cluster_beat_refs.update(ref for ref in refs if isinstance(ref, str))
            if any(ref not in beat_ids for ref in refs):
                failures.append(f"CLUSTER_{index + 1}_BEAT_REFERENCE_BROKEN")

    scene_cluster_refs: list[str] = []
    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            failures.append(f"SCENE_{index + 1}_INVALID")
            continue
        missing = [field for field in SCENE_REQUIRED_FIELDS if not _present(scene.get(field))]
        if missing:
            failures.append(f"SCENE_{index + 1}_FIELDS_MISSING:{','.join(missing)}")
        refs = scene.get("payload_cluster_refs")
        if isinstance(refs, list):
            scene_cluster_refs.extend(ref for ref in refs if isinstance(ref, str))
            if any(ref not in cluster_ids for ref in refs):
                failures.append(f"SCENE_{index + 1}_CLUSTER_REFERENCE_BROKEN")

    if mode in CHAPTER_MODES:
        minimum_beats = 6 if strict else 4
        minimum_clusters = 3 if strict else 2
        minimum_scenes = 3 if strict else 2
        if len(core_beats) < minimum_beats:
            failures.append("CHAPTER_PAYLOAD_SHORTFALL" if strict else "STAGEABLE_CORE_BEAT_SHORTFALL")
        if len(clusters) < minimum_clusters:
            failures.append("CHAPTER_PAYLOAD_SHORTFALL" if strict else "PAYLOAD_CLUSTER_SHORTFALL")
        if len(scenes) < minimum_scenes:
            failures.append("CHAPTER_PAYLOAD_SHORTFALL" if strict else "CORE_SCENE_SHORTFALL")
        if strict:
            active_actors = {str(beat.get("active_actor")) for beat in core_beats if _present(beat.get("active_actor"))}
            information_updates = [beat.get("new_information_or_choice") for beat in core_beats if _present(beat.get("new_information_or_choice"))]
            delta_dimensions: set[str] = set()
            for beat in core_beats:
                delta = beat.get("delta")
                if isinstance(delta, dict):
                    delta_dimensions.update(str(key) for key in delta)
                elif _present(delta):
                    delta_dimensions.add("delta")
            actions = [str(beat.get("action")) for beat in core_beats if _present(beat.get("action"))]
            if len(active_actors) < 2:
                failures.append("CHAPTER_ACTOR_DIVERSITY_SHORTFALL")
            if len(information_updates) < 2:
                failures.append("CHAPTER_INFORMATION_SHORTFALL")
            if len(delta_dimensions) < 2:
                failures.append("CHAPTER_INFORMATION_SHORTFALL")
            if len(actions) != len(set(actions)):
                failures.append("CHAPTER_DUPLICATE_ACTION")
            core_beat_ids = {beat.get("beat_id") for beat in core_beats if isinstance(beat.get("beat_id"), str)}
            if not core_beat_ids.issubset(cluster_beat_refs):
                failures.append("CHAPTER_BEAT_CLUSTER_COVERAGE")
            if len(scene_cluster_refs) < minimum_clusters or len(scene_cluster_refs) != len(set(scene_cluster_refs)):
                failures.append("CHAPTER_SCENE_CLUSTER_COVERAGE")
            beat_deltas = [_canonical_json(beat.get("delta")) for beat in core_beats if _present(beat.get("delta"))]
            if len(beat_deltas) != len(set(beat_deltas)):
                failures.append("CHAPTER_DUPLICATE_DELTA")

    roles = {str(beat.get("beat_role", "")).upper() for beat in core_beats}
    middle_roles = {"ACTION", "COUNTERMOVE", "REPLAN", "COST"}

    # 支持经典四步法或网文起承转合/施压-反转-兑现/高潮循环
    INITIATION_ROLES = {"ACTION", "SETUP", "PRESSURE", "CONFRONTATION", "DISCOVERY", "PROMISE"}
    TURNING_ROLES = {"COUNTERMOVE", "REPLAN", "ESCALATION", "TURN", "CRISIS", "COMPLICATION", "STRUGGLE"}
    PAYOFF_ROLES = {"COST", "CLIMAX", "PAYOFF", "FACE_SLAP", "REVELATION", "HOOK", "RESOLUTION", "SACRIFICE"}

    has_webnovel_progression = (
        len(roles) >= 3
        and any(r in INITIATION_ROLES for r in roles)
        and any(r in TURNING_ROLES for r in roles)
        and any(r in PAYOFF_ROLES for r in roles)
    )

    missing_middle_roles = sorted(middle_roles - roles) if not (middle_roles.issubset(roles) or has_webnovel_progression) else []
    if missing_middle_roles:
        failures.append("MID_CHAPTER_LOAD_FAILED")

    return {
        "chapter_id": entity.get("id"),
        "target_prose_range": target_range,
        "stageable_core_beats": len(core_beats),
        "supporting_stageable_beats": len(supporting_beats),
        "summary_result_beats_removed": removed,
        "payload_clusters": len(clusters),
        "core_scenes": len(scenes),
        "mid_chapter_load": "PASS" if not missing_middle_roles else "FAIL",
        "missing_middle_roles": missing_middle_roles,
        "writer_core_plot_invention_required": bool(failures),
        "final_capacity": "FULL" if not failures else "THIN",
        "failure_reasons": sorted(set(failures)),
    }


def audit_chapter_set(packet: dict) -> list[dict]:
    """Check whole-book chapter coverage only when the packet explicitly requests it."""
    precision = packet.get("precision") if isinstance(packet, dict) else {}
    if not isinstance(precision, dict):
        return []
    if _is_final_full_book(packet) and precision.get("full_book_detailed_required") is not True:
        return [_issue("FULL_BOOK_MODE_REQUIRED", "FINAL_FULL_BOOK requires full_book_detailed_required=true")]
    if precision.get("full_book_detailed_required") is not True:
        return []
    plans = [
        entity for entity in packet.get("entities", [])
        if isinstance(entity, dict) and str(entity.get("kind", "")).upper() == "CHAPTER_PLAN"
    ]
    if not plans:
        return [_issue("CHAPTER_PLAN_MISSING", "full-book detailed mode requires at least one ChapterPlan")]
    errors: list[dict] = []
    numbers: list[int] = []
    for entity in plans:
        payload = entity.get("payload") if isinstance(entity.get("payload"), dict) else {}
        if str(payload.get("plan_level", "STORY_NODE")).upper() != "PRODUCTION_READY":
            errors.append(_issue("CHAPTER_NOT_PRODUCTION_READY", "full-book detailed mode requires PRODUCTION_READY chapters", entity.get("id")))
        number = payload.get("chapter_no")
        if not isinstance(number, int) or number < 1:
            errors.append(_issue("INVALID_CHAPTER_NUMBER", "chapter_no must be a positive integer", entity.get("id")))
        else:
            numbers.append(number)
    if len(numbers) != len(set(numbers)):
        errors.append(_issue("DUPLICATE_CHAPTER_NUMBER", "chapter_no must be unique"))
    expected = precision.get("expected_chapters")
    if expected is None:
        errors.append(_issue("EXPECTED_CHAPTERS_REQUIRED", "full-book detailed mode requires expected_chapters"))
    elif not isinstance(expected, int) or expected < 1:
        errors.append(_issue("INVALID_EXPECTED_CHAPTERS", "expected_chapters must be a positive integer"))
    elif numbers:
        target = expected if isinstance(expected, int) else max(numbers)
        required = set(range(1, target + 1))
        actual = set(numbers)
        for number in sorted(required - actual):
            errors.append(_issue("CHAPTER_PLAN_MISSING", f"chapter {number} has no ChapterPlan"))
        for number in sorted(actual - required):
            errors.append(_issue("CHAPTER_NUMBER_OUT_OF_RANGE", f"chapter {number} exceeds expected chapter count"))
    return errors


def audit_packet(packet: dict) -> AuditReport:
    """Run deterministic checks that do not require literary interpretation."""
    errors: list[dict] = []
    warnings: list[dict] = []
    if not isinstance(packet, dict):
        return AuditReport([_issue("INVALID_PACKET", "packet must be an object")], warnings)
    packet_mode = packet.get("packet_mode", "SNAPSHOT")
    if not isinstance(packet_mode, str) or packet_mode.upper() not in PACKET_MODES:
        errors.append(_issue("INVALID_PACKET_MODE", "packet_mode must be SNAPSHOT or PATCH"))
    entities = packet.get("entities")
    edges = packet.get("edges")
    if not isinstance(entities, list) or not isinstance(edges, list):
        return AuditReport([_issue("INVALID_PACKET", "entities and edges must be lists")], warnings)
    if "negative_facts" in packet and not isinstance(packet["negative_facts"], list):
        errors.append(_issue("INVALID_PACKET", "negative_facts must be a list"))
    elif isinstance(packet.get("negative_facts"), list) and any(not isinstance(fact, str) for fact in packet["negative_facts"]):
        errors.append(_issue("INVALID_PACKET", "negative_facts entries must be strings"))
    for key in ("assumptions", "open_questions", "source_refs"):
        if key in packet and not isinstance(packet[key], list):
            errors.append(_issue("INVALID_PACKET", f"{key} must be a list"))
        elif isinstance(packet.get(key), list) and any(not isinstance(value, str) for value in packet[key]):
            errors.append(_issue("INVALID_PACKET", f"{key} entries must be strings"))
    if "precision" in packet and not isinstance(packet["precision"], dict):
        errors.append(_issue("INVALID_PACKET", "precision must be an object"))
    source_registry = packet.get("provenance_registry")
    if source_registry is not None and not isinstance(source_registry, (dict, list)):
        errors.append(_issue("INVALID_PACKET", "provenance_registry must be an object or list"))
    if isinstance(source_registry, list) and any(not isinstance(value, str) for value in source_registry):
        errors.append(_issue("INVALID_PACKET", "provenance_registry list entries must be strings"))
    known_sources = set(
        source_registry if isinstance(source_registry, list) and all(isinstance(value, str) for value in source_registry)
        else (source_registry.keys() if isinstance(source_registry, dict) else [])
    )

    entity_map: dict[str, dict] = {}
    for entity in entities:
        if not isinstance(entity, dict) or not isinstance(entity.get("id"), str) or not entity["id"]:
            errors.append(_issue("INVALID_ENTITY", "entity requires a non-empty id"))
            continue
        entity_id = entity["id"]
        if entity_id in entity_map:
            errors.append(_issue("DUPLICATE_ID", "duplicate entity id", entity_id))
            continue
        entity_map[entity_id] = entity
        kind = str(entity.get("kind", "UNKNOWN")).upper()
        name = str(entity.get("name", ""))
        namespace = str(entity.get("namespace", "PLAN")).upper()
        status = str(entity.get("status", "ACTIVE")).upper()
        if namespace not in ALLOWED_NAMESPACES:
            errors.append(_issue("INVALID_NAMESPACE", "namespace must be CONTRACT, CANON, or PLAN", entity_id))
        if status not in ALLOWED_STATUSES:
            errors.append(_issue("INVALID_STATUS", "status is not a recognized Canon status", entity_id))
        payload = entity.get("payload")
        if not isinstance(payload, dict):
            errors.append(_issue("INVALID_PAYLOAD", "entity payload must be an object", entity_id))
            payload = {}
        if kind in {"CHAR", "CHARACTER", "PERSON"}:
            if not name or name in PLACEHOLDER_NAMES or any(name.startswith(prefix) and name[-1:] in "一二三四五六七八九AB" for prefix in ("官员", "护卫", "商人", "弟子", "村民")):
                errors.append(_issue("PLACEHOLDER_PERSON", "individual actor must have a real name", entity_id))
            if any(not payload.get(field) for field in REQUIRED_CHARACTER_FIELDS):
                errors.append(_issue("CHARACTER_WITHOUT_AGENCY", "character needs identity, desire, interest, constraints, and strategy", entity_id))
            tier = str(payload.get("character_tier", "SUPPORT")).upper()
            if tier not in {"CORE", "MAJOR", "SUPPORT", "EPHEMERAL", "COHORT"}:
                errors.append(_issue("INVALID_CHARACTER_TIER", "character_tier must be CORE, MAJOR, SUPPORT, EPHEMERAL, or COHORT", entity_id))
            if tier in {"CORE", "MAJOR"} and any(not payload.get(field) for field in REQUIRED_LIFE_PROFILE_FIELDS):
                errors.append(_issue("CHARACTER_LIFE_PROFILE_MISSING", "core/major character needs biography, private life, decision model, arc, fate, and highlights", entity_id))
        if kind in PROVENANCE_KINDS and not payload.get("provenance_refs"):
            errors.append(_issue("MISSING_PROVENANCE", "important entity needs provenance_refs", entity_id))
        if "provenance_refs" in payload and not isinstance(payload.get("provenance_refs"), list):
            errors.append(_issue("INVALID_PROVENANCE", "provenance_refs must be a list", entity_id))
        if known_sources and isinstance(payload.get("provenance_refs"), list):
            for ref in payload["provenance_refs"]:
                if ref not in known_sources:
                    errors.append(_issue("UNKNOWN_PROVENANCE", "provenance reference is absent from provenance_registry", entity_id))

    edge_map: dict[str, dict] = {}
    adjacency: dict[str, list[str]] = {}
    for edge in edges:
        if not isinstance(edge, dict) or not isinstance(edge.get("id"), str) or not edge["id"]:
            errors.append(_issue("INVALID_EDGE", "edge requires a non-empty id"))
            continue
        edge_id = edge["id"]
        if edge_id in edge_map:
            errors.append(_issue("DUPLICATE_ID", "duplicate edge id", edge_id))
            continue
        edge_map[edge_id] = edge
        edge_namespace = str(edge.get("namespace", "PLAN")).upper()
        edge_status = str(edge.get("status", "ACTIVE")).upper()
        if edge_namespace not in ALLOWED_NAMESPACES:
            errors.append(_issue("INVALID_NAMESPACE", "namespace must be CONTRACT, CANON, or PLAN", edge_id))
        if edge_status not in ALLOWED_STATUSES:
            errors.append(_issue("INVALID_STATUS", "status is not a recognized Canon status", edge_id))
        if not isinstance(edge.get("payload", {}), dict):
            errors.append(_issue("INVALID_PAYLOAD", "edge payload must be an object", edge_id))
        source, target = edge.get("source"), edge.get("target")
        if source not in entity_map or target not in entity_map:
            errors.append(_issue("BROKEN_REFERENCE", "edge endpoint does not exist", edge_id))
            continue
        edge_type = str(edge.get("type", "")).upper()
        if edge_type in CAUSAL_EDGE_TYPES:
            adjacency.setdefault(source, []).append(target)

    packet_precision = packet.get("precision") if isinstance(packet.get("precision"), dict) else {}
    strict_full_book = _is_final_full_book(packet) and packet_precision.get("full_book_detailed_required") is True
    for entity_id, entity in entity_map.items():
        kind = str(entity.get("kind", "UNKNOWN")).upper()
        payload = entity.get("payload") if isinstance(entity.get("payload"), dict) else {}
        if kind == "EVENT":
            actor = payload.get("active_actor") or payload.get("world_process_id")
            if not actor or actor not in entity_map:
                errors.append(_issue("ORPHAN_EVENT", "event needs an existing active_actor or world process", entity_id))
            elif not any(
                edge.get("target") == entity_id
                and str(edge.get("type", "")).upper() == "PARTICIPATES_IN"
                and edge.get("source") == actor
                for edge in edge_map.values()
            ):
                errors.append(_issue("UNLINKED_CAUSAL_ACTOR", "event actor must participate in the event", entity_id))
            if not payload.get("provenance_refs"):
                errors.append(_issue("MISSING_PROVENANCE", "event needs provenance_refs", entity_id))
            if not payload.get("causal_inputs") or not payload.get("causal_outputs"):
                errors.append(_issue("EVENT_CAUSAL_FIELDS_MISSING", "event needs causal_inputs and causal_outputs", entity_id))
            if not payload.get("action") or not payload.get("state_delta"):
                errors.append(_issue("EVENT_ACTION_MISSING", "event needs an action and a state delta", entity_id))
            for field in ("causal_inputs", "causal_outputs"):
                refs = payload.get(field, [])
                if isinstance(refs, list):
                    for ref in refs:
                        if ref not in entity_map:
                            errors.append(_issue("BROKEN_REFERENCE", f"event {field} references an unknown entity", entity_id))
            causal_pairs = {
                (edge.get("source"), edge.get("target"))
                for edge in edge_map.values()
                if str(edge.get("type", "")).upper() in {"CAUSES", "RESULTS_IN"}
            }
            for ref in payload.get("causal_inputs", []) if isinstance(payload.get("causal_inputs"), list) else []:
                if str(entity_map.get(ref, {}).get("kind", "")).upper() == "EVENT" and (ref, entity_id) not in causal_pairs:
                    errors.append(_issue("CAUSAL_INPUT_EDGE_MISSING", "event causal input needs a matching CAUSES/RESULTS_IN edge", entity_id))
            for ref in payload.get("causal_outputs", []) if isinstance(payload.get("causal_outputs"), list) else []:
                if str(entity_map.get(ref, {}).get("kind", "")).upper() == "EVENT" and (entity_id, ref) not in causal_pairs:
                    errors.append(_issue("CAUSAL_OUTPUT_EDGE_MISSING", "event causal output needs a matching CAUSES/RESULTS_IN edge", entity_id))
            for field in ("location",):
                ref = payload.get(field)
                if ref and ref not in entity_map:
                    errors.append(_issue("BROKEN_REFERENCE", f"event {field} references an unknown entity", entity_id))
            if "time_index" in payload and not isinstance(payload.get("time_index"), (int, float)):
                errors.append(_issue("INVALID_TIME_INDEX", "event time_index must be numeric", entity_id))
            for ref in payload.get("line_refs", []) if isinstance(payload.get("line_refs"), list) else []:
                if ref not in entity_map:
                    errors.append(_issue("BROKEN_REFERENCE", "event line_refs references an unknown line", entity_id))
            if payload.get("requires_hyperedge"):
                participants = [
                    edge for edge in edge_map.values()
                    if edge.get("target") == entity_id and str(edge.get("type", "")).upper() == "PARTICIPATES_IN"
                ]
                if len(participants) < 2:
                    errors.append(_issue("HYPEREDGE_PARTICIPANT_SHORTFALL", "compound event needs at least two participants", entity_id))
                if len({edge.get("source") for edge in participants}) < 2:
                    errors.append(_issue("HYPEREDGE_DUPLICATE_PARTICIPANT", "compound event needs distinct participants", entity_id))
                roles = {edge.get("payload", {}).get("role") for edge in participants if isinstance(edge.get("payload"), dict)}
                if "initiator" not in roles:
                    errors.append(_issue("HYPEREDGE_INITIATOR_MISSING", "compound event needs an initiator role", entity_id))
        if kind == "LINE":
            if not payload.get("owner"):
                errors.append(_issue("UNOWNED_NARRATIVE_LINE", "line needs an owner", entity_id))
            elif payload["owner"] not in entity_map:
                errors.append(_issue("BROKEN_REFERENCE", "line owner does not exist", entity_id))
            if not payload.get("closure_condition"):
                errors.append(_issue("UNCLOSED_MAJOR_LINE", "line needs a closure condition", entity_id))
            line_status = str(payload.get("status", entity.get("status", "ACTIVE"))).upper()
            if line_status in {"CLOSED", "RESOLVED", "PAID_OFF"} and not payload.get("closure_event"):
                errors.append(_issue("CLOSED_LINE_WITHOUT_EVENT", "closed line needs a closure_event", entity_id))
        if kind == "PROMISE":
            required = ("creation_event", "maturity_condition", "reveal_window", "payoff_event")
            if any(not payload.get(field) for field in required):
                errors.append(_issue("UNRESOLVED_CORE_PROMISE", "promise needs creation, maturity, reveal, and payoff", entity_id))
            for field in ("creation_event", "payoff_event"):
                ref = payload.get(field)
                if ref and ref not in entity_map:
                    errors.append(_issue("BROKEN_REFERENCE", f"promise {field} references an unknown entity", entity_id))
            promise_status = str(payload.get("status", entity.get("status", "ACTIVE"))).upper()
            if promise_status in {"PAID_OFF", "RESOLVED"} and not payload.get("payoff_event"):
                errors.append(_issue("PAID_PROMISE_WITHOUT_PAYOFF", "paid-off promise needs a payoff_event", entity_id))
            for field in ("who_knows", "who_misunderstands", "reinforcement_events", "choices_affected"):
                refs = payload.get(field, [])
                if isinstance(refs, list):
                    for ref in refs:
                        if ref not in entity_map:
                            errors.append(_issue("BROKEN_REFERENCE", f"promise {field} references an unknown entity", entity_id))

        if kind == "CHAPTER_PLAN":
            level = str(payload.get("plan_level", "STORY_NODE")).upper()
            if level not in {"STORY_NODE", "DETAILED_PLAN", "PRODUCTION_READY"}:
                errors.append(_issue("INVALID_PLAN_LEVEL", "plan_level must be STORY_NODE, DETAILED_PLAN, or PRODUCTION_READY", entity_id))
            missing = [field for field in CHAPTER_PLAN_REQUIRED_FIELDS if not _present(payload.get(field))]
            if missing:
                errors.append(_issue("CHAPTER_CONTRACT_MISSING", f"chapter plan needs: {', '.join(missing)}", entity_id))
            capacity = audit_chapter_capacity(entity, strict=strict_full_book)
            if level == "PRODUCTION_READY" and capacity["final_capacity"] != "FULL":
                for reason in capacity["failure_reasons"]:
                    errors.append(_issue(reason, reason, entity_id))
                errors.append(_issue("CAPACITY_GATE_FAILED", "; ".join(capacity["failure_reasons"]), entity_id))
                if strict_full_book:
                    errors.append(_issue("CHAPTER_PAYLOAD_SHORTFALL", "; ".join(capacity["failure_reasons"]), entity_id))
        elif kind == "BEAT":
            level = str(payload.get("plan_level", "STORY_NODE")).upper()
            if level not in {"STORY_NODE", "DETAILED_PLAN", "PRODUCTION_READY"}:
                errors.append(_issue("INVALID_PLAN_LEVEL", "plan_level must be STORY_NODE, DETAILED_PLAN, or PRODUCTION_READY", entity_id))
        if kind == "HUMAN_STATE":
            required = ("bodily_state", "daily_routine", "social_obligations", "immediate_need")
            if any(not payload.get(field) for field in required):
                errors.append(_issue("HUMAN_REALITY_PROFILE_MISSING", "human state needs body, routine, obligations, and immediate need", entity_id))

    errors.extend(audit_outline_scope(packet))
    errors.extend(audit_chapter_set(packet))

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            errors.append(_issue("CAUSAL_CYCLE", "causal event graph contains a cycle", node))
            return
        if node in visited:
            return
        visiting.add(node)
        for child in adjacency.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for node in adjacency:
        visit(node)

    for edge in edge_map.values():
        if str(edge.get("type", "")).upper() != "PRECEDES":
            continue
        source = entity_map.get(edge.get("source"), {})
        target = entity_map.get(edge.get("target"), {})
        source_p = source.get("payload") if isinstance(source.get("payload"), dict) else {}
        target_p = target.get("payload") if isinstance(target.get("payload"), dict) else {}
        source_time = source_p.get("time_index")
        target_time = target_p.get("time_index")
        if isinstance(source_time, (int, float)) and isinstance(target_time, (int, float)) and source_time > target_time:
            errors.append(_issue("CAUSAL_ORDER_CONFLICT", "PRECEDES edge runs backward in story time", edge.get("id")))

    # 全局因果拓扑时序反转检查 (Global Topological Causal Time Inversion Check)
    time_indexed_nodes = [
        node_id for node_id, ent in entity_map.items()
        if isinstance(ent.get("payload"), dict) and isinstance(ent["payload"].get("time_index"), (int, float))
    ]
    for start_node in time_indexed_nodes:
        start_payload = entity_map[start_node].get("payload")
        if not isinstance(start_payload, dict):
            continue
        start_time = start_payload.get("time_index")
        if not isinstance(start_time, (int, float)):
            continue
        queue = list(adjacency.get(start_node, []))
        seen = set(queue)
        while queue:
            curr = queue.pop(0)
            curr_payload = entity_map.get(curr, {}).get("payload")
            curr_time = curr_payload.get("time_index") if isinstance(curr_payload, dict) else None
            if isinstance(curr_time, (int, float)) and start_time > curr_time:
                # 检查是否已由直接 PRECEDES 报错，避免重复报告相同两节点
                direct_precedes = any(
                    e.get("source") == start_node and e.get("target") == curr and str(e.get("type", "")).upper() == "PRECEDES"
                    for e in edge_map.values()
                )
                if not direct_precedes:
                    errors.append(_issue(
                        "CAUSAL_ORDER_CONFLICT",
                        f"causal predecessor '{start_node}' (time_index={start_time}) causally precedes '{curr}' (time_index={curr_time}) but occurs later in story time",
                        start_node,
                    ))
                break
            for nxt in adjacency.get(curr, []):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)

    return AuditReport(errors, warnings, {
        "entities": len(entity_map), "edges": len(edge_map),
        "errors": len(errors), "warnings": len(warnings),
    })


def build_context_from_packet(packet: dict, anchors: list[str], max_hops: int = 2) -> dict:
    """Build a bounded, provenance-preserving context without inventing facts."""
    entities = {item["id"]: item for item in packet.get("entities", []) if isinstance(item, dict) and item.get("id")}
    edges = [item for item in packet.get("edges", []) if isinstance(item, dict)]
    missing = [anchor for anchor in anchors if anchor not in entities]
    adjacency: dict[str, set[str]] = {}
    for edge in edges:
        source, target = edge.get("source"), edge.get("target")
        if source in entities and target in entities:
            adjacency.setdefault(source, set()).add(target)
            adjacency.setdefault(target, set()).add(source)

    reachable = set(anchors)
    frontier = set(anchors)
    for _ in range(max(0, max_hops)):
        next_frontier = set().union(*(adjacency.get(node, set()) for node in frontier)) if frontier else set()
        next_frontier -= reachable
        reachable |= next_frontier
        frontier = next_frontier

    def entity_kind(kind: str | set[str]) -> list[dict]:
        kinds = {kind} if isinstance(kind, str) else {value.upper() for value in kind}
        return [
            entities[entity_id]
            for entity_id in sorted(reachable)
            if entity_id in entities and str(entities[entity_id].get("kind", "")).upper() in kinds
        ]

    hyperedges: list[dict] = []
    role_order = {"initiator": 0, "target": 1, "evidence": 2, "location": 3}
    for event in sorted(entity_kind("EVENT"), key=lambda item: item["id"]):
        participants = []
        for edge in edges:
            if edge.get("target") != event["id"] or str(edge.get("type", "")).upper() != "PARTICIPATES_IN":
                continue
            if edge.get("source") not in entities:
                continue
            payload = edge.get("payload") if isinstance(edge.get("payload"), dict) else {}
            participants.append({
                "id": edge["source"],
                "kind": entities[edge["source"]].get("kind"),
                "role": payload.get("role", "participant"),
                "edge_id": edge.get("id"),
            })
        if participants:
            participants.sort(key=lambda item: (role_order.get(item["role"], 99), item["id"]))
            hyperedges.append({"event_id": event["id"], "participants": participants})

    relevant_edges = sorted([
        edge for edge in edges
        if edge.get("source") in reachable or edge.get("target") in reachable
    ], key=lambda item: item.get("id", ""))
    hard_canon = [
        entities[entity_id] for entity_id in sorted(reachable)
        if entity_id in entities and str(entities[entity_id].get("namespace", "")).upper() == "CANON"
    ]
    plan = [
        entities[entity_id] for entity_id in sorted(reachable)
        if entity_id in entities and str(entities[entity_id].get("namespace", "")).upper() == "PLAN"
    ]
    negative_facts = sorted(str(fact) for fact in packet.get("negative_facts", []))
    missing_sections = []
    if missing:
        missing_sections.append("anchors")
    if not hard_canon and not plan:
        missing_sections.append("state")
    if not hyperedges and any(str(entity.get("kind", "")).upper() == "EVENT" for entity in plan):
        missing_sections.append("event_participants")
    return {
        "assumptions": list(packet.get("assumptions", [])),
        "open_questions": list(packet.get("open_questions", [])),
        "source_refs": list(packet.get("source_refs", [])),
        "precision": dict(packet.get("precision", {})),
        "hard_canon": hard_canon,
        "plan": plan,
        "character_states": entity_kind({"CHARACTER", "CHAR", "PERSON", "COHORT"}),
        "relationships": relevant_edges,
        "causal_paths": [edge for edge in relevant_edges if str(edge.get("type", "")).upper() in CAUSAL_EDGE_TYPES],
        "active_lines": entity_kind("LINE"),
        "promises": entity_kind("PROMISE"),
        "timeline_facts": sorted(
            [entities[entity] for entity in reachable if entity in entities and "time_index" in (entities[entity].get("payload") or {})],
            key=lambda item: ((item.get("payload") or {}).get("time_index", float("inf")), item["id"]),
        ),
        "hyperedges": hyperedges,
        "negative_facts": negative_facts,
        "provenance_refs": sorted({ref for entity_id in reachable if entity_id in entities for ref in (entities[entity_id].get("payload") or {}).get("provenance_refs", [])}),
        "retrieval_sufficiency": "SUFFICIENT" if not missing_sections else "INSUFFICIENT",
        "missing": missing_sections,
    }


def build_context_with_graph(
    packet: dict,
    project_id: str,
    anchors: list[str],
    max_hops: int = 2,
    source: str = "auto",
    projector: GraphProjector | None = None,
) -> dict:
    """Prefer Neo4j retrieval when requested, with an explicit local fallback."""
    if source not in {"sqlite", "neo4j", "auto"}:
        raise ValidationError("context source must be sqlite, neo4j, or auto", "INVALID_CONTEXT_SOURCE")
    context = build_context_from_packet(packet, anchors, max_hops)
    context["retrieval_source"] = "SQLITE"
    if source == "sqlite":
        return context
    projector = projector or GraphProjector()
    try:
        rows = []
        for anchor in anchors:
            rows.extend(projector.query("character_neighborhood", {"project_id": project_id, "anchor_id": anchor}))
        context["graph_retrieval"] = rows
        context["retrieval_source"] = "NEO4J"
        context["graph_status"] = {"status": "OK"}
        return context
    except ValidationError as error:
        if source == "neo4j":
            raise
        context["graph_status"] = {"status": "DEGRADED", "code": error.code, "message": str(error)}
        return context


SCHEMA = """
CREATE TABLE IF NOT EXISTS projects(
  project_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entities(
  project_id TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  namespace TEXT NOT NULL,
  status TEXT NOT NULL,
  name TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY(project_id, entity_id),
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS edges(
  project_id TEXT NOT NULL,
  edge_id TEXT NOT NULL,
  edge_type TEXT NOT NULL,
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  namespace TEXT NOT NULL,
  status TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY(project_id, edge_id),
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS commits(
  project_id TEXT NOT NULL,
  version INTEGER NOT NULL,
  parent_version INTEGER,
  message TEXT NOT NULL,
  snapshot_hash TEXT NOT NULL,
  snapshot_json TEXT,
  created_at TEXT NOT NULL,
  PRIMARY KEY(project_id, version),
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS changes(
  change_id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id TEXT NOT NULL,
  version INTEGER NOT NULL,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  action TEXT NOT NULL,
  before_json TEXT,
  after_json TEXT NOT NULL,
  projection_status TEXT NOT NULL DEFAULT 'PENDING',
  projection_error TEXT,
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS negative_facts(
  project_id TEXT NOT NULL,
  fact TEXT NOT NULL,
  PRIMARY KEY(project_id, fact),
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
CREATE TABLE IF NOT EXISTS packet_metadata(
  project_id TEXT PRIMARY KEY,
  assumptions_json TEXT NOT NULL,
  open_questions_json TEXT NOT NULL,
  source_refs_json TEXT NOT NULL,
  precision_json TEXT NOT NULL,
  provenance_registry_json TEXT NOT NULL DEFAULT '{}',
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);
"""


class CanonicalStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.executescript(SCHEMA)
        commit_columns = {row[1] for row in connection.execute("PRAGMA table_info(commits)")}
        if "snapshot_json" not in commit_columns:
            connection.execute("ALTER TABLE commits ADD COLUMN snapshot_json TEXT")
        metadata_columns = {row[1] for row in connection.execute("PRAGMA table_info(packet_metadata)")}
        if "provenance_registry_json" not in metadata_columns:
            connection.execute("ALTER TABLE packet_metadata ADD COLUMN provenance_registry_json TEXT NOT NULL DEFAULT '{}'")
        return connection

    @staticmethod
    def _snapshot(packet: dict) -> dict:
        return {
            "packet_mode": "SNAPSHOT",
            "entities": sorted(packet.get("entities", []), key=lambda item: item["id"]),
            "edges": sorted(packet.get("edges", []), key=lambda item: item["id"]),
            "negative_facts": sorted(set(packet.get("negative_facts", []))),
            "assumptions": list(packet.get("assumptions", [])),
            "open_questions": list(packet.get("open_questions", [])),
            "source_refs": list(packet.get("source_refs", [])),
            "precision": dict(packet.get("precision", {})),
            "provenance_registry": packet.get("provenance_registry", {}),
        }

    @staticmethod
    def _merge_patch(base: dict, patch: dict) -> dict:
        def merge_items(key: str) -> list[dict]:
            combined = {item["id"]: item for item in base.get(key, [])}
            combined.update({item["id"]: item for item in patch.get(key, [])})
            return sorted(combined.values(), key=lambda item: item["id"])

        negative_facts = (
            patch["negative_facts"] if "negative_facts" in patch
            else base.get("negative_facts", [])
        )
        merged = {
            "packet_mode": "SNAPSHOT",
            "entities": merge_items("entities"),
            "edges": merge_items("edges"),
            "negative_facts": sorted(set(negative_facts)),
        }
        for key, default in (("assumptions", []), ("open_questions", []), ("source_refs", []), ("precision", {})):
            merged[key] = patch[key] if key in patch else base.get(key, default)

        base_registry = base.get("provenance_registry", {})
        patch_registry = patch.get("provenance_registry")
        if patch_registry is None:
            merged["provenance_registry"] = base_registry
        elif isinstance(base_registry, dict) and isinstance(patch_registry, dict):
            combined_registry = dict(base_registry)
            combined_registry.update(patch_registry)
            merged["provenance_registry"] = combined_registry
        elif isinstance(base_registry, list) and isinstance(patch_registry, list):
            merged["provenance_registry"] = sorted(set(base_registry + patch_registry))
        else:
            merged["provenance_registry"] = patch_registry
        return merged

    def init_project(self, project_id: str, title: str) -> int:
        if not project_id or not title:
            raise ValidationError("project_id and title are required", "PROJECT_FIELDS_REQUIRED")
        now = _now()
        empty_snapshot = self._snapshot({"entities": [], "edges": [], "negative_facts": []})
        empty_hash = _sha256(empty_snapshot)
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT version FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if existing is not None:
                return int(existing["version"])
            connection.execute(
                "INSERT INTO projects(project_id,title,version,created_at,updated_at) VALUES(?,?,?,?,?)",
                (project_id, title, 0, now, now),
            )
            empty_snapshot_json = _canonical_json(empty_snapshot)
            connection.execute(
                "INSERT INTO commits(project_id,version,parent_version,message,snapshot_hash,snapshot_json,created_at) VALUES(?,?,?,?,?,?,?)",
                (project_id, 0, None, "init", empty_hash, empty_snapshot_json, now),
            )
        return 0

    def get_version(self, project_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT version FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
        if row is None:
            raise ValidationError(f"unknown project: {project_id}", "PROJECT_NOT_FOUND", project_id)
        return int(row["version"])

    def load_snapshot(self, project_id: str, version: int | None = None) -> dict:
        with self._connect() as connection:
            project = connection.execute(
                "SELECT version FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if project is None:
                raise ValidationError(f"unknown project: {project_id}", "PROJECT_NOT_FOUND", project_id)
            target = int(project["version"] if version is None else version)
            row = connection.execute(
                "SELECT snapshot_json FROM commits WHERE project_id = ? AND version = ?",
                (project_id, target),
            ).fetchone()
        if row is None:
            raise ValidationError(f"unknown version: {target}", "VERSION_NOT_FOUND", project_id)
        if not row["snapshot_json"]:
            raise ValidationError(f"snapshot is unavailable for version {target}", "SNAPSHOT_UNAVAILABLE", project_id)
        return json.loads(row["snapshot_json"])

    @staticmethod
    def _validate_packet_shape(packet: dict) -> None:
        if not isinstance(packet, dict):
            raise ValidationError("packet must be an object", "INVALID_PACKET")
        for key in ("entities", "edges"):
            if not isinstance(packet.get(key), list):
                raise ValidationError(f"packet.{key} must be a list", "INVALID_PACKET")
        for collection, key in ((packet["entities"], "id"), (packet["edges"], "id")):
            seen: set[str] = set()
            for item in collection:
                if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key]:
                    raise ValidationError(f"every {key} entry must be a non-empty string", "INVALID_PACKET")
                if item[key] in seen:
                    raise ValidationError(f"duplicate id: {item[key]}", "DUPLICATE_ID", item[key])
                seen.add(item[key])
        mode = packet.get("packet_mode", "SNAPSHOT")
        if not isinstance(mode, str) or mode.upper() not in PACKET_MODES:
            raise ValidationError("packet_mode must be SNAPSHOT or PATCH", "INVALID_PACKET_MODE")
        for key in ("negative_facts", "assumptions", "open_questions", "source_refs"):
            if key in packet and not isinstance(packet[key], list):
                raise ValidationError(f"packet.{key} must be a list", "INVALID_PACKET")
            if key in packet and any(not isinstance(value, str) for value in packet[key]):
                raise ValidationError(f"packet.{key} entries must be strings", "INVALID_PACKET")
        if "precision" in packet and not isinstance(packet["precision"], dict):
            raise ValidationError("packet.precision must be an object", "INVALID_PACKET")
        registry = packet.get("provenance_registry")
        if registry is not None and not isinstance(registry, (dict, list)):
            raise ValidationError("packet.provenance_registry must be an object or list", "INVALID_PACKET")
        if isinstance(registry, list) and any(not isinstance(value, str) for value in registry):
            raise ValidationError("packet.provenance_registry entries must be strings", "INVALID_PACKET")

    @staticmethod
    def _entity_row(project_id: str, item: dict) -> tuple[str, str, str, str, str, str, str]:
        payload = item.get("payload", {})
        if not isinstance(payload, dict):
            raise ValidationError("entity payload must be an object", "INVALID_PAYLOAD", item["id"])
        return (
            project_id,
            item["id"],
            str(item.get("kind", "UNKNOWN")),
            str(item.get("namespace", "PLAN")),
            str(item.get("status", "ACTIVE")),
            str(item.get("name", item["id"])),
            _canonical_json(payload),
        )

    @staticmethod
    def _edge_row(project_id: str, item: dict) -> tuple[str, str, str, str, str, str, str, str]:
        payload = item.get("payload", {})
        if not isinstance(payload, dict):
            raise ValidationError("edge payload must be an object", "INVALID_PAYLOAD", item["id"])
        source = item.get("source")
        target = item.get("target")
        if not isinstance(source, str) or not isinstance(target, str):
            raise ValidationError("edge source and target are required", "EDGE_ENDPOINT_REQUIRED", item["id"])
        return (
            project_id,
            item["id"],
            str(item.get("type", "RELATED_TO")),
            source,
            target,
            str(item.get("namespace", "PLAN")),
            str(item.get("status", "ACTIVE")),
            _canonical_json(payload),
        )

    def apply_packet(
        self, project_id: str, packet: dict, expected_version: int, message: str
    ) -> CommitResult:
        self._validate_packet_shape(packet)
        mode = str(packet.get("packet_mode", "SNAPSHOT")).upper()
        effective_packet = packet
        if mode == "PATCH":
            _, base_packet = self._load_packet(project_id)
            effective_packet = self._merge_patch(base_packet, packet)
        report = audit_packet(effective_packet)
        if not report.ok:
            first = report.errors[0]
            raise ValidationError(first["message"], first["code"], first.get("object_id"))
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            project = connection.execute(
                "SELECT version FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if project is None:
                raise ValidationError(f"unknown project: {project_id}", "PROJECT_NOT_FOUND", project_id)
            current_version = int(project["version"])
            if current_version != expected_version:
                raise ValidationError(
                    f"expected version {expected_version}, found {current_version}",
                    "VERSION_CONFLICT",
                    project_id,
                )

            snapshot = self._snapshot(effective_packet)
            snapshot_hash = _sha256(snapshot)
            latest = connection.execute(
                "SELECT snapshot_hash FROM commits WHERE project_id = ? AND version = ?",
                (project_id, current_version),
            ).fetchone()
            if latest is not None and latest["snapshot_hash"] == snapshot_hash:
                return CommitResult(project_id, current_version, snapshot_hash, 0)

            next_version = current_version + 1
            changes: list[tuple[str, str, str, str | None, str]] = []
            entity_rows = [self._entity_row(project_id, item) for item in effective_packet["entities"]]
            edge_rows = [self._edge_row(project_id, item) for item in effective_packet["edges"]]

            if mode == "SNAPSHOT":
                wanted_entities = {row[1] for row in entity_rows}
                old_entities = connection.execute(
                    "SELECT * FROM entities WHERE project_id = ?", (project_id,)
                ).fetchall()
                for old in old_entities:
                    if old["entity_id"] in wanted_entities:
                        continue
                    before = json.dumps(dict(old), ensure_ascii=False, sort_keys=True)
                    connection.execute(
                        "DELETE FROM entities WHERE project_id = ? AND entity_id = ?",
                        (project_id, old["entity_id"]),
                    )
                    changes.append(("ENTITY", old["entity_id"], "DELETE", before, "{}"))
                wanted_edges = {row[1] for row in edge_rows}
                old_edges = connection.execute(
                    "SELECT * FROM edges WHERE project_id = ?", (project_id,)
                ).fetchall()
                for old in old_edges:
                    if old["edge_id"] in wanted_edges:
                        continue
                    before = json.dumps(dict(old), ensure_ascii=False, sort_keys=True)
                    connection.execute(
                        "DELETE FROM edges WHERE project_id = ? AND edge_id = ?",
                        (project_id, old["edge_id"]),
                    )
                    changes.append(("EDGE", old["edge_id"], "DELETE", before, "{}"))

            for row in entity_rows:
                old = connection.execute(
                    "SELECT * FROM entities WHERE project_id = ? AND entity_id = ?",
                    (project_id, row[1]),
                ).fetchone()
                before = json.dumps(dict(old), ensure_ascii=False, sort_keys=True) if old else None
                connection.execute(
                    """INSERT INTO entities(project_id,entity_id,kind,namespace,status,name,payload_json)
                    VALUES(?,?,?,?,?,?,?)
                    ON CONFLICT(project_id,entity_id) DO UPDATE SET
                      kind=excluded.kind, namespace=excluded.namespace, status=excluded.status,
                      name=excluded.name, payload_json=excluded.payload_json""",
                    row,
                )
                after = json.dumps(
                    {
                        "project_id": row[0],
                        "entity_id": row[1],
                        "kind": row[2],
                        "namespace": row[3],
                        "status": row[4],
                        "name": row[5],
                        "payload_json": row[6],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                changed = old is None or any(
                    old[column] != value
                    for column, value in (
                        ("kind", row[2]), ("namespace", row[3]), ("status", row[4]),
                        ("name", row[5]), ("payload_json", row[6]),
                    )
                )
                if changed:
                    changes.append(("ENTITY", row[1], "UPSERT", before, after))

            for row in edge_rows:
                old = connection.execute(
                    "SELECT * FROM edges WHERE project_id = ? AND edge_id = ?",
                    (project_id, row[1]),
                ).fetchone()
                before = json.dumps(dict(old), ensure_ascii=False, sort_keys=True) if old else None
                connection.execute(
                    """INSERT INTO edges(project_id,edge_id,edge_type,source_id,target_id,namespace,status,payload_json)
                    VALUES(?,?,?,?,?,?,?,?)
                    ON CONFLICT(project_id,edge_id) DO UPDATE SET
                      edge_type=excluded.edge_type, source_id=excluded.source_id,
                      target_id=excluded.target_id, namespace=excluded.namespace,
                      status=excluded.status, payload_json=excluded.payload_json""",
                    row,
                )
                after = json.dumps(
                    {
                        "project_id": row[0],
                        "edge_id": row[1],
                        "edge_type": row[2],
                        "source_id": row[3],
                        "target_id": row[4],
                        "namespace": row[5],
                        "status": row[6],
                        "payload_json": row[7],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                changed = old is None or any(
                    old[column] != value
                    for column, value in (
                        ("edge_type", row[2]), ("source_id", row[3]), ("target_id", row[4]),
                        ("namespace", row[5]), ("status", row[6]), ("payload_json", row[7]),
                    )
                )
                if changed:
                    changes.append(("EDGE", row[1], "UPSERT", before, after))

            connection.execute("DELETE FROM negative_facts WHERE project_id = ?", (project_id,))
            negative_facts = effective_packet.get("negative_facts", [])
            if not isinstance(negative_facts, list):
                raise ValidationError("packet.negative_facts must be a list", "INVALID_PACKET")
            connection.executemany(
                "INSERT INTO negative_facts(project_id, fact) VALUES(?, ?)",
                [(project_id, fact) for fact in sorted(set(negative_facts))],
            )
            assumptions = effective_packet.get("assumptions", [])
            open_questions = effective_packet.get("open_questions", [])
            source_refs = effective_packet.get("source_refs", [])
            precision = effective_packet.get("precision", {})
            if not all(isinstance(value, list) for value in (assumptions, open_questions, source_refs)):
                raise ValidationError("assumptions, open_questions, and source_refs must be lists", "INVALID_PACKET")
            if not isinstance(precision, dict):
                raise ValidationError("precision must be an object", "INVALID_PACKET")
            connection.execute(
                """INSERT INTO packet_metadata(project_id, assumptions_json, open_questions_json,
                   source_refs_json, precision_json, provenance_registry_json) VALUES(?,?,?,?,?,?)
                   ON CONFLICT(project_id) DO UPDATE SET
                     assumptions_json=excluded.assumptions_json,
                     open_questions_json=excluded.open_questions_json,
                     source_refs_json=excluded.source_refs_json,
                     precision_json=excluded.precision_json,
                     provenance_registry_json=excluded.provenance_registry_json""",
                (
                    project_id,
                    _canonical_json(assumptions),
                    _canonical_json(open_questions),
                    _canonical_json(source_refs),
                    _canonical_json(precision),
                    _canonical_json(effective_packet.get("provenance_registry", {})),
                ),
            )

            now = _now()
            connection.execute(
                "INSERT INTO commits(project_id,version,parent_version,message,snapshot_hash,snapshot_json,created_at) VALUES(?,?,?,?,?,?,?)",
                (project_id, next_version, current_version, message, snapshot_hash, _canonical_json(snapshot), now),
            )
            connection.executemany(
                """INSERT INTO changes(project_id,version,object_type,object_id,action,before_json,after_json)
                VALUES(?,?,?,?,?,?,?)""",
                [(project_id, next_version, *change) for change in changes],
            )
            connection.execute(
                "UPDATE projects SET version = ?, updated_at = ? WHERE project_id = ?",
                (next_version, now, project_id),
            )
        return CommitResult(project_id, next_version, snapshot_hash, len(changes))

    def _load_packet(self, project_id: str) -> tuple[str, dict]:
        with self._connect() as connection:
            project = connection.execute(
                "SELECT title FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if project is None:
                raise ValidationError(f"unknown project: {project_id}", "PROJECT_NOT_FOUND", project_id)
            entity_rows = connection.execute(
                "SELECT * FROM entities WHERE project_id = ? ORDER BY entity_id", (project_id,)
            ).fetchall()
            edge_rows = connection.execute(
                "SELECT * FROM edges WHERE project_id = ? ORDER BY edge_id", (project_id,)
            ).fetchall()
            negative_rows = connection.execute(
                "SELECT fact FROM negative_facts WHERE project_id = ? ORDER BY fact", (project_id,)
            ).fetchall()
            metadata = connection.execute(
                "SELECT * FROM packet_metadata WHERE project_id = ?", (project_id,)
            ).fetchone()
        entities = []
        for row in entity_rows:
            entities.append({
                "id": row["entity_id"], "kind": row["kind"], "namespace": row["namespace"],
                "status": row["status"], "name": row["name"], "payload": json.loads(row["payload_json"]),
            })
        edges = []
        for row in edge_rows:
            edges.append({
                "id": row["edge_id"], "type": row["edge_type"], "source": row["source_id"],
                "target": row["target_id"], "namespace": row["namespace"], "status": row["status"],
                "payload": json.loads(row["payload_json"]),
            })
        packet = {
            "entities": entities,
            "edges": edges,
            "negative_facts": [str(row["fact"]) for row in negative_rows],
        }
        if metadata is not None:
            packet.update({
                "assumptions": json.loads(metadata["assumptions_json"]),
                "open_questions": json.loads(metadata["open_questions_json"]),
                "source_refs": json.loads(metadata["source_refs_json"]),
                "precision": json.loads(metadata["precision_json"]),
                "provenance_registry": json.loads(metadata["provenance_registry_json"] or "{}"),
            })
        return str(project["title"]), packet

    def pending_changes(self, project_id: str) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM changes WHERE project_id = ? AND projection_status IN ('PENDING', 'DEGRADED') ORDER BY change_id",
                (project_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def mark_projection(self, change_ids: list[int], status: str, error: str | None = None) -> None:
        if status not in {"APPLIED", "DEGRADED"}:
            raise ValidationError("invalid projection status", "INVALID_PROJECTION_STATUS")
        with self._connect() as connection:
            connection.executemany(
                "UPDATE changes SET projection_status = ?, projection_error = ? WHERE change_id = ?",
                [(status, error, change_id) for change_id in change_ids],
            )

    def rebuild_changes(self, project_id: str) -> int:
        """Queue a complete Canon projection without changing the Canon version."""
        with self._connect() as connection:
            project = connection.execute(
                "SELECT version FROM projects WHERE project_id = ?", (project_id,)
            ).fetchone()
            if project is None:
                raise ValidationError(f"unknown project: {project_id}", "PROJECT_NOT_FOUND", project_id)
            version = int(project["version"])
            pending_keys = {
                (row["object_type"], row["object_id"], int(row["version"]))
                for row in connection.execute(
                    "SELECT object_type, object_id, version FROM changes WHERE project_id = ? AND projection_status IN ('PENDING', 'DEGRADED')",
                    (project_id,),
                )
            }
            rows: list[tuple] = []
            for row in connection.execute(
                "SELECT * FROM entities WHERE project_id = ? ORDER BY entity_id", (project_id,)
            ):
                after = json.dumps(dict(row), ensure_ascii=False, sort_keys=True)
                if ("ENTITY", row["entity_id"], version) not in pending_keys:
                    rows.append((project_id, version, "ENTITY", row["entity_id"], "UPSERT", None, after))
            for row in connection.execute(
                "SELECT * FROM edges WHERE project_id = ? ORDER BY edge_id", (project_id,)
            ):
                after = json.dumps(dict(row), ensure_ascii=False, sort_keys=True)
                if ("EDGE", row["edge_id"], version) not in pending_keys:
                    rows.append((project_id, version, "EDGE", row["edge_id"], "UPSERT", None, after))
            connection.executemany(
                """INSERT INTO changes(project_id,version,object_type,object_id,action,before_json,after_json)
                VALUES(?,?,?,?,?,?,?)""",
                rows,
            )
        return len(rows)

    def export_markdown(self, project_id: str, output_path: Path) -> Path:
        title, packet = self._load_packet(project_id)
        content = render_packet_markdown(packet, title=title, project_id=project_id)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".outline-", suffix=".tmp", dir=output_path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(content)
            os.replace(temporary, output_path)
        except Exception:
            Path(temporary).unlink(missing_ok=True)
            raise
        return output_path

    def export_audit(self, project_id: str, output_path: Path) -> Path:
        title, packet = self._load_packet(project_id)
        report = audit_packet(packet)
        _append_graph_health(report, self.pending_changes(project_id), project_id)
        lines = [f"# Audit Report: {title}", "", f"- project_id: `{project_id}`", f"- ok: `{report.ok}`", f"- counts: `{json.dumps(report.counts or {}, ensure_ascii=False, sort_keys=True)}`", "", "## Errors", ""]
        lines.extend(f"- `{item['code']}` `{item.get('object_id') or ''}`: {item['message']}" for item in report.errors)
        if not report.errors:
            lines.append("- None")
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- `{item['code']}` `{item.get('object_id') or ''}`: {item['message']}" for item in report.warnings)
        if not report.warnings:
            lines.append("- None")
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".audit-", suffix=".tmp", dir=output_path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write("\n".join(lines) + "\n")
            os.replace(temporary, output_path)
        except Exception:
            Path(temporary).unlink(missing_ok=True)
            raise
        return output_path


SECTION_ORDER = (
    ("项目总契约与禁止事项", {"PROJECT"}),
    ("世界观与风格宪法", {"RULE"}),
    ("世界规则、时代、技术或力量上限", {"RULE"}),
    ("地理、交通、通信、资源与信息网络", {"LOCATION", "RESOURCE"}),
    ("势力和机构生态", {"FACTION"}),
    ("全人物总表", {"CHARACTER", "COHORT"}),
    ("核心与重要人物生平、性格成因和决策模型", {"CHARACTER", "HUMAN_STATE"}),
    ("人物关系拓扑", {"CHARACTER", "RELATION"}),
    ("人物弧、高光与命运地图", {"CHARACTER"}),
    ("N 幕宏观结构", {"ACT"}),
    ("Dynamic N-Line 总图", {"LINE"}),
    ("多线碰撞矩阵", {"LINE"}),
    ("全书剧情梗概", {"EVENT"}),
    ("全书主因果链", {"EVENT"}),
    ("伏笔、悬念、揭示和兑现地图", {"PROMISE"}),
    ("全书时间线", {"EVENT", "TIMEPOINT"}),
    ("空间、移动、资源和信息流", {"LOCATION", "RESOURCE"}),
    ("高潮、低谷和规则变化地图", {"CLIMAX"}),
    ("卷级架构与每卷因果脊柱", {"VOLUME"}),
    ("全章 Story Nodes", {"EVENT", "BEAT"}),
    ("指定窗口详细章纲", {"EVENT", "CHAPTER_PLAN"}),
    ("关键人物、道具、证据、地点和规则来源表", {"CHARACTER", "OBJECT", "PROP", "EVIDENCE", "LOCATION", "RULE"}),
    ("开放余波与禁止漂移清单", {"LINE", "PROMISE", "RULE"}),
)


def _format_readable_value(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, list):
        if not val:
            return "（无）"
        if all(isinstance(x, str) for x in val):
            return "、".join(val)
        return json.dumps(val, ensure_ascii=False)
    if isinstance(val, dict):
        return json.dumps(val, ensure_ascii=False)
    return str(val)


def render_packet_markdown(packet: dict, title: str = "VNext Outline", project_id: str = "PROJECT.unknown") -> str:
    entities = {item["id"]: item for item in packet.get("entities", [])}
    entity_names = {item_id: item.get("name", item_id) for item_id, item in entities.items()}

    def readable_ref(value: Any) -> str:
        if isinstance(value, str) and value in entity_names:
            return entity_names[value]
        return str(value) if value is not None else ""

    projects = [item for item in entities.values() if str(item.get("kind", "")).upper() == "PROJECT"]
    document_title = projects[0].get("name") if projects else title
    lines = [f"# {document_title}", "", f"- project_id: `{project_id}`", "- source: `SQLite Canon`", ""]
    for label, key in (("假设", "assumptions"), ("开放问题", "open_questions"), ("来源", "source_refs")):
        values = packet.get(key, [])
        lines.append(f"- {label}: " + ("；".join(str(value) for value in values) if values else "（无）"))
    precision = packet.get("precision", {})
    lines.append(f"- 精度: `{json.dumps(precision, ensure_ascii=False, sort_keys=True)}`")
    report = audit_packet(packet)
    final_book = _is_final_full_book(packet)
    complete = final_book and isinstance(precision, dict) and precision.get("full_book_detailed_required") is True and not report.errors
    status = "COMPLETE" if complete else ("INCOMPLETE" if final_book else "INTERMEDIATE")
    chapter_plans = [item for item in entities.values() if str(item.get("kind", "")).upper() == "CHAPTER_PLAN"]
    lines.append(f"- 大纲状态: `{status}` | 声明卷数: `{precision.get('expected_volumes', '未声明') if isinstance(precision, dict) else '未声明'}` | 声明章数: `{precision.get('expected_chapters', '未声明') if isinstance(precision, dict) else '未声明'}` | 已有详细章数: `{len(chapter_plans)}`")
    lines.append("")
    emitted: set[str] = set()

    def format_project_readable(item: dict) -> list[str]:
        payload = item.get("payload", {})
        return [
            f"- **一句话总纲**: {payload.get('one_sentence_synopsis', '（缺失）')}",
            f"- **前因—发展—结局因果总纲**: {payload.get('causal_summary', '（缺失）')}",
            f"- **原创化差异约束**: {_format_readable_value(payload.get('originality_axes', '未声明'))}",
        ]

    def format_volume_readable(item: dict) -> list[str]:
        payload = item.get("payload", {})
        res = [f"### `{item['id']}` **{item.get('name', item['id'])}**（第{payload.get('chapter_start', '?')}—{payload.get('chapter_end', '?')}章）"]
        res.append(f"- **卷级详细剧情**: {payload.get('detailed_plot', '（缺失）')}")
        res.append(f"- **核心冲突**: {payload.get('central_conflict', '（缺失）')}")
        res.append(f"- **关键转折**: {_format_readable_value(payload.get('turning_points'))}")
        res.append(f"- **卷末结算**: {payload.get('payoff', '（缺失）')}")
        res.append(f"- **下一卷钩子**: {payload.get('next_hook', '（缺失）')}")
        return res

    def format_character_readable(item: dict) -> list[str]:
        p = item.get("payload", {})
        res = [f"- `{item['id']}` **{item.get('name', item['id'])}** [{p.get('identity', '未指定身份')}]"]
        res.append(f"  * **人物层级**: `{p.get('character_tier', 'SUPPORT')}` | **核心欲望**: {_format_readable_value(p.get('desires'))} | **阶段目标**: {_format_readable_value(p.get('goals'))}")
        if p.get("biography"):
            res.append(f"  * **人物生平与成因**: {p['biography']}")
        if p.get("personality"):
            res.append(f"  * **性格特质**: {p['personality']} | **行为策略**: {p.get('preferred_strategy', '未定义')}")
        if p.get("decision_model"):
            res.append(f"  * **决策模型**: {p['decision_model']}")
        if p.get("private_life") or p.get("life_constraints"):
            res.append(f"  * **现实生活与羁绊**: {p.get('private_life', '无')} | **现实约束**: {_format_readable_value(p.get('life_constraints'))}")
        if p.get("knowledge_state") or p.get("misjudgments"):
            res.append(f"  * **认知边界与信息盲区**: {p.get('knowledge_state', '完整')} | **误判**: {_format_readable_value(p.get('misjudgments'))}")
        if p.get("arc") or p.get("growth_arc"):
            res.append(f"  * **成长弧光**: {p.get('arc') or p.get('growth_arc')}")
        if p.get("highlights"):
            res.append(f"  * **人物高光时刻**: {_format_readable_value(p.get('highlights'))}")
        if p.get("fate"):
            res.append(f"  * **最终命运与归宿**: {p['fate']}")
        return res

    def format_event_readable(item: dict) -> list[str]:
        p = item.get("payload", {})
        res = [f"### `{item['id']}` **{item.get('name', item['id'])}**"]
        res.append(f"- **主导者/行动方**: `{p.get('active_actor', '环境/世界过程')}` | **发生地点**: `{p.get('location', '未指定')}` | **时间窗口**: `{p.get('time_window', p.get('time_index', '默认'))}`")
        if p.get("action"):
            res.append(f"- **核心行动**: {p['action']}")
        if p.get("choice") or p.get("cost"):
            res.append(f"- **所作抉择**: {p.get('choice', '常规反应')} | **付出代价**: {p.get('cost', '无')}")
        if p.get("state_delta"):
            res.append(f"- **产生状态变化(Delta)**: {p['state_delta']}")
        inputs = "、".join(f"`{x}`" for x in p.get("causal_inputs", [])) if p.get("causal_inputs") else "（起始）"
        outputs = "、".join(f"`{x}`" for x in p.get("causal_outputs", [])) if p.get("causal_outputs") else "（终结）"
        res.append(f"- **因果链**: {inputs} $\\longrightarrow$ {outputs}")
        return res

    def format_line_readable(item: dict) -> list[str]:
        p = item.get("payload", {})
        res = [f"### `{item['id']}` **{item.get('name', item['id'])}** (状态: `{p.get('status', item.get('status', 'ACTIVE'))}`)"]
        res.append(f"- **Line Owner**: `{p.get('owner', '未知')}` | **主线诉求**: {p.get('goal', '未指定')}")
        if p.get("pressure") or p.get("opposing_force"):
            res.append(f"- **外部压强与对抗力量**: {p.get('pressure', '')} | 对抗方: {p.get('opposing_force', '')}")
        if p.get("milestones"):
            res.append(f"- **里程碑演进**: {_format_readable_value(p.get('milestones'))}")
        if p.get("climax_condition") or p.get("closure_condition"):
            res.append(f"- **高潮触发**: {p.get('climax_condition', '无')} | **闭环结算条件**: {p.get('closure_condition', '无')}")
        return res

    def format_promise_readable(item: dict) -> list[str]:
        p = item.get("payload", {})
        res = [f"### `{item['id']}` **{item.get('name', item['id'])}** (状态: `{p.get('status', item.get('status', 'ACTIVE'))}`)"]
        res.append(f"- **埋设事件**: `{p.get('creation_event', '')}` $\\to$ **揭示窗口**: `{p.get('reveal_window', '')}` $\\to$ **兑现事件**: `{p.get('payoff_event', '')}`")
        if p.get("who_knows") or p.get("who_misunderstands"):
            res.append(f"- **信息差博弈**: 先知者 `{_format_readable_value(p.get('who_knows'))}` vs 误解/受蒙蔽者 `{_format_readable_value(p.get('who_misunderstands'))}`")
        if p.get("maturity_condition"):
            res.append(f"- **成熟发酵条件**: {p['maturity_condition']}")
        if p.get("post_payoff_state"):
            res.append(f"- **兑现后余波与爽点结算**: {p['post_payoff_state']}")
        return res

    def format_chapter_plan_readable(item: dict) -> list[str]:
        p = item.get("payload", {})
        cap = audit_chapter_capacity(item, strict=_is_final_full_book(packet))
        res = [f"### 第 {p.get('chapter_no', '?')} 章: `{item['id']}` **{item.get('name', item['id'])}** (所属卷: `{p.get('volume_ref', '')}` | 评级: `{cap.get('final_capacity')}`)", ""]
        res.append(f"- **章节功能定位**: {p.get('chapter_function', '未定义')}")
        res.append(f"- **核心不可逆状态变化(Core Delta)**: {p.get('core_delta', '无')}")
        if p.get("conflict_contract"):
            cc = p["conflict_contract"]
            res.append(f"- **戏剧矛盾对峙**: `{readable_ref(cc.get('actor_a'))}` vs `{readable_ref(cc.get('actor_b'))}` —— 核心不可调和点: {cc.get('concrete_incompatibility', '')}")
        if p.get("dynamic_beats"):
            res.append("- **动态节拍链 (Dynamic Beats)**:")
            for b in p["dynamic_beats"]:
                res.append(f"  * **[{b.get('beat_id', '')} - {b.get('beat_role', 'BEAT')}]**: `{readable_ref(b.get('active_actor'))}`行动 `{b.get('action', '')}` $\\to$ 对手反制 `{b.get('counterforce', '')}` $\\to$ 带来变化: {_format_readable_value(b.get('delta'))}")
        if p.get("scene_payloads"):
            res.append("- **场景对峙切片 (Scene Payloads)**:")
            for sc in p["scene_payloads"]:
                res.append(f"  * `{sc.get('scene_id')}`: 入口 `{sc.get('entry_state')}` $\\to$ 对峙焦点 `{sc.get('immediate_stakes')}` $\\to$ 出口 `{sc.get('exit_state')}`")
        if p.get("continuation_source"):
            res.append(f"- **章末继续力 / 悬念钩子**: {p.get('continuation_source')}")
        if p.get("forbidden_drift"):
            res.append(f"- **禁止漂移与水文约束**: {_format_readable_value(p.get('forbidden_drift'))}")
        res.append(f"- **容量审计与抗水审查**: `capacity_audit={json.dumps(cap, ensure_ascii=False, sort_keys=True)}`")
        return res

    project_items = [item for item in entities.values() if str(item.get("kind", "")).upper() == "PROJECT"]
    lines.extend(["# 全书一句话总纲", ""])
    if project_items:
        lines.extend(format_project_readable(project_items[0]))
        emitted.add(project_items[0]["id"])
    else:
        lines.append("- （缺少 PROJECT 总纲）")
    lines.append("")

    volume_items = [item for item in entities.values() if str(item.get("kind", "")).upper() == "VOLUME"]
    lines.extend(["# 卷级详细剧情", ""])
    for item in sorted(volume_items, key=lambda value: ((value.get("payload") or {}).get("chapter_start", 10**9), value["id"])):
        lines.extend(format_volume_readable(item))
        lines.append("")
        emitted.add(item["id"])
    if not volume_items:
        lines.append("- （缺少卷级详细剧情）")
    lines.append("")

    lines.extend(["# 全章目录与推进表", ""])
    for item in sorted(chapter_plans, key=lambda value: ((value.get("payload") or {}).get("chapter_no", 10**9), value["id"])):
        payload = item.get("payload", {})
        lines.append(
            f"- **第{payload.get('chapter_no', '?')}章《{item.get('name', item['id'])}》** | 卷 `{readable_ref(payload.get('volume_ref'))}` | 人物 `{readable_ref(payload.get('conflict_contract', {}).get('actor_a'))}` vs `{readable_ref(payload.get('conflict_contract', {}).get('actor_b'))}` | {payload.get('chapter_function', '')} | Delta: {payload.get('core_delta', '')} | 钩子: {payload.get('continuation_source', '')}"
        )
    if not chapter_plans:
        lines.append("- （缺少逐章目录）")
    lines.append("")

    def payload_readable_block(item: dict) -> list[str]:
        kind = str(item.get("kind", "")).upper()
        if kind in {"CHARACTER", "CHAR"}:
            return format_character_readable(item)
        if kind == "EVENT":
            return format_event_readable(item)
        if kind == "LINE":
            return format_line_readable(item)
        if kind == "PROMISE":
            return format_promise_readable(item)
        if kind == "CHAPTER_PLAN":
            return format_chapter_plan_readable(item)
        p = item.get("payload", {})
        res = [f"- `{item['id']}` **{item.get('name', item['id'])}** [{kind}]"]
        for k, v in sorted(p.items()):
            res.append(f"  * **{k}**: {_format_readable_value(v)}")
        return res

    for heading, kinds in SECTION_ORDER:
        lines.extend([f"# {heading}", ""])
        selected = [item for item in entities.values() if str(item.get("kind", "")).upper() in kinds and item["id"] not in emitted]
        roster = heading == "全人物总表"
        if heading == "指定窗口详细章纲":
            selected.sort(key=lambda value: ((value.get("payload") or {}).get("chapter_no", 10**9), value["id"]))
        elif heading == "卷级架构与每卷因果脊柱":
            selected.sort(key=lambda value: ((value.get("payload") or {}).get("chapter_start", 10**9), value["id"]))
        elif heading == "全书剧情梗概":
            selected.sort(key=lambda value: ((value.get("payload") or {}).get("time_index", 10**9), value["id"]))
        else:
            selected.sort(key=lambda value: value["id"])
        for item in selected:
            if roster and str(item.get("kind", "")).upper() == "COHORT":
                p = item.get("payload", {})
                lines.append(f"- `{item['id']}` **{item.get('name', item['id'])}** [群体/阵营] — {json.dumps(p, ensure_ascii=False)}")
                emitted.add(item["id"])
            elif roster and str(item.get("kind", "")).upper() in {"CHARACTER", "CHAR"}:
                identity = (item.get("payload") or {}).get("identity", "")
                tier = (item.get("payload") or {}).get("character_tier", "SUPPORT")
                lines.append(f"- `{item['id']}` **{item.get('name', item['id'])}** [{tier} | {identity}]")
            else:
                lines.extend(payload_readable_block(item))
                lines.append("")
                emitted.add(item["id"])
        if not selected:
            matching = [item for item in entities.values() if str(item.get("kind", "")).upper() in kinds]
            lines.append("- （条目已在前置章节展开）" if matching else "- （本阶段暂无已提交条目）")
        lines.append("")

    lines.extend(["# 负事实与禁止漂移", ""])
    negative_facts = sorted(packet.get("negative_facts", []))
    if negative_facts:
        lines.extend(f"- `{fact}`" for fact in negative_facts)
    else:
        lines.append("- （暂无负事实）")
    lines.append("")

    lines.extend(["# 关系与因果边", ""])
    names = {item_id: item.get("name", item_id) for item_id, item in entities.items()}
    for edge in sorted(packet.get("edges", []), key=lambda value: value["id"]):
        lines.append(f"- `{edge['id']}` `{edge.get('type', 'RELATED_TO')}`: **{names.get(edge.get('source'), edge.get('source'))}** $\\to$ **{names.get(edge.get('target'), edge.get('target'))}** — {json.dumps(edge.get('payload', {}), ensure_ascii=False, sort_keys=True)}")
    if not packet.get("edges"):
        lines.append("- （暂无关系边）")
    return "\n".join(lines) + "\n"


def _cypher_literal(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        escaped = (
            value.replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
        return "'" + escaped + "'"
    if isinstance(value, (list, tuple, set)):
        return "[" + ", ".join(_cypher_literal(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(f"{key}: {_cypher_literal(item)}" for key, item in value.items()) + "}"
    raise TypeError(f"unsupported Cypher parameter type: {type(value)!r}")


class GraphProjector:
    EDGE_PREFLIGHT = (
        "UNWIND $edges AS row "
        "OPTIONAL MATCH (s:Entity {id: row.source, project_id: $project_id}), "
        "(t:Entity {id: row.target, project_id: $project_id}) "
        "WITH row, s, t WHERE s IS NULL OR t IS NULL "
        "RETURN row.id AS edge_id, row.source AS source_id, row.target AS target_id"
    )

    QUERY_TEXTS = {
        "character_neighborhood": (
            "MATCH (a:Entity {id: $anchor_id, project_id: $project_id})-[r:REL*1..2]-(n:Entity {project_id: $project_id}) "
            "WHERE all(x IN r WHERE x.project_id = $project_id) "
            "RETURN a.id AS anchor_id, n.id AS node_id, "
            "[x IN r | {type:x.type, edge_id:x.edge_id}] AS path"
        ),
        "causal_path": (
            "MATCH p=(a:Entity {id:$from_id, project_id:$project_id})-[:REL*1..8]->(b:Entity {id:$to_id, project_id:$project_id}) "
            "WHERE all(x IN relationships(p) WHERE x.project_id = $project_id AND x.type IN "
            "['CAUSES', 'ENABLES', 'BLOCKS', 'REQUIRES']) "
            "RETURN [x IN nodes(p) | x.id] AS node_ids"
        ),
        "hyperedge_context": (
            "MATCH (e:Entity {kind:'EVENT', id:$event_id, project_id:$project_id})<-[r:REL {type:'PARTICIPATES_IN', project_id:$project_id}]-(p:Entity {project_id:$project_id}) "
            "RETURN e.id AS event_id, collect({id:p.id, role:r.role, kind:p.kind}) AS participants"
        ),
    }

    def __init__(self, shell: str = "cypher-shell", database: str = "neo4j", timeout_seconds: float = 15.0):
        self.shell = shell
        self.database = database
        self.timeout_seconds = timeout_seconds
        self.graph_dir = Path(__file__).resolve().parents[1] / "graph"

    def _resolved_shell(self) -> str:
        resolved = shutil.which(self.shell)
        if resolved:
            return resolved
        if Path(self.shell).is_file():
            return self.shell
        raise ValidationError("cypher-shell was not found", "NEO4J_SHELL_NOT_FOUND")

    def _run(self, cypher: str, params: dict | None = None) -> str:
        shell = self._resolved_shell()
        username = os.environ.get("NEO4J_USERNAME", os.environ.get("NEO4J_USER"))
        password = os.environ.get("NEO4J_PASSWORD")
        if not username or not password:
            raise ValidationError(
                "NEO4J_USERNAME/NEO4J_PASSWORD are required for graph operations",
                "NEO4J_CONFIG_MISSING",
            )
        address = os.environ.get("NEO4J_URI", os.environ.get("NEO4J_ADDRESS", "neo4j://localhost:7687"))
        parsed_address = urlparse(address)
        if parsed_address.hostname not in {"localhost", "127.0.0.1", "::1"} and os.environ.get("NEO4J_ALLOW_REMOTE") != "1":
            raise ValidationError("remote Neo4j endpoints are disabled; set NEO4J_ALLOW_REMOTE=1 explicitly", "NEO4J_REMOTE_BLOCKED")
        command = [
            shell, "--non-interactive", "--format", "plain", "-a", address,
            "-u", username, "-d", self.database,
        ]
        if params:
            command.extend(["-P", _cypher_literal(params)])
        try:
            result = subprocess.run(
                command,
                input=cypher,
                text=True,
                capture_output=True,
                check=False,
                timeout=self.timeout_seconds,
                env={**os.environ, "NEO4J_PASSWORD": password},
            )
        except subprocess.TimeoutExpired as error:
            raise ValidationError(
                f"Neo4j command exceeded {self.timeout_seconds:g}s", "NEO4J_TIMEOUT"
            ) from error
        if result.returncode:
            raise ValidationError(
                result.stderr.strip() or "Neo4j query failed", "NEO4J_QUERY_FAILED"
            )
        return result.stdout

    def ensure_schema(self) -> None:
        schema = (self.graph_dir / "constraints.cypher").read_text(encoding="utf-8")
        self._run(schema)

    def query_text(self, script_name: str) -> str:
        if script_name not in self.QUERY_TEXTS:
            raise ValidationError(f"query is not allowlisted: {script_name}", "QUERY_NOT_ALLOWED")
        return self.QUERY_TEXTS[script_name]

    def sync(self, project_id: str, changes: list[dict]) -> ProjectionResult:
        if not changes:
            return ProjectionResult(0, [])
        entities: list[dict] = []
        edges: list[dict] = []
        delete_entities: list[dict] = []
        delete_edges: list[dict] = []
        versions = []
        for change in changes:
            after = change.get("after_json")
            if isinstance(after, str):
                after = json.loads(after)
            before = change.get("before_json")
            if isinstance(before, str):
                before = json.loads(before)
            if change.get("action") == "DELETE":
                target = before or {"entity_id": change.get("object_id"), "edge_id": change.get("object_id")}
                if change.get("object_type") == "ENTITY":
                    delete_entities.append({"id": target.get("entity_id", change.get("object_id"))})
                elif change.get("object_type") == "EDGE":
                    delete_edges.append({"id": target.get("edge_id", change.get("object_id"))})
                versions.append(int(change.get("version", 0)))
                continue
            if change.get("object_type") == "ENTITY":
                payload = json.loads(after.get("payload_json", "{}"))
                entities.append({
                    "id": after["entity_id"],
                    "kind": after["kind"],
                    "props": {
                        "project_id": project_id, "kind": after["kind"], "name": after["name"],
                        "namespace": after["namespace"], "status": after["status"],
                        "payload": _canonical_json(payload),
                    },
                })
            elif change.get("object_type") == "EDGE":
                payload = json.loads(after.get("payload_json", "{}"))
                edges.append({
                    "id": after["edge_id"], "type": after["edge_type"],
                    "source": after["source_id"], "target": after["target_id"],
                    "props": {
                        "project_id": project_id, "type": after["edge_type"],
                        "namespace": after["namespace"], "status": after["status"],
                        "role": payload.get("role") if isinstance(payload, dict) else None,
                        "payload": _canonical_json(payload),
                    },
                })
            versions.append(int(change.get("version", 0)))
        cypher = (self.graph_dir / "projection.cypher").read_text(encoding="utf-8")
        self.ensure_schema()
        preflight = self._run(self.EDGE_PREFLIGHT, {
            "project_id": project_id,
            "edges": edges,
        })
        rows = list(csv.reader(io.StringIO(preflight), delimiter="\t"))
        if len(rows) > 1:
            edge_id = rows[1][0] if rows[1] else "unknown"
            raise ValidationError(
                f"Neo4j edge endpoint is missing for {edge_id}", "NEO4J_ENDPOINT_MISSING", edge_id
            )
        self._run(cypher, {
            "project_id": project_id,
            "canon_version": max(versions or [0]),
            "entities": entities,
            "edges": edges,
            "delete_entities": delete_entities,
            "delete_edges": delete_edges,
        })
        return ProjectionResult(len(changes), [])

    def rebuild(self, project_id: str, changes: list[dict]) -> ProjectionResult:
        self.ensure_schema()
        self._run(
            "MATCH (n:Entity {project_id:$project_id}) DETACH DELETE n",
            {"project_id": project_id},
        )
        return self.sync(project_id, changes)

    def query(self, script_name: str, params: dict) -> list[dict]:
        query_params = dict(params)
        if "anchor_ids" in query_params:
            anchor_ids = query_params.pop("anchor_ids")
            if not isinstance(anchor_ids, list) or not anchor_ids:
                raise ValidationError("anchor_ids must be a non-empty list", "INVALID_QUERY_PARAMS")
            query_params["anchor_id"] = anchor_ids[0]
        output = self._run(self.query_text(script_name), query_params)
        rows = list(csv.reader(io.StringIO(output), delimiter="\t"))
        if not rows:
            return []
        headers = rows[0]
        return [dict(zip(headers, row)) for row in rows[1:] if row]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VNext long-form outline runtime")
    subparsers = parser.add_subparsers(dest="command")
    init = subparsers.add_parser("init")
    init.add_argument("--db", required=True)
    init.add_argument("--project-id", required=True)
    init.add_argument("--title", required=True)

    apply = subparsers.add_parser("apply")
    apply.add_argument("--db", required=True)
    apply.add_argument("--project-id", required=True)
    apply.add_argument("--expected-version", required=True, type=int)
    apply.add_argument("--packet", required=True)
    apply.add_argument("--message", required=True)

    context = subparsers.add_parser("context")
    context.add_argument("--db", required=True)
    context.add_argument("--project-id", required=True)
    context.add_argument("--anchor", action="append", required=True)
    context.add_argument("--max-hops", type=int, default=2)
    context.add_argument("--source", choices=("sqlite", "neo4j", "auto"), default="auto")

    audit = subparsers.add_parser("audit")
    audit.add_argument("--db")
    audit.add_argument("--project-id")
    audit.add_argument("--packet")

    sync = subparsers.add_parser("graph-sync")
    sync.add_argument("--db", required=True)
    sync.add_argument("--project-id", required=True)

    rebuild = subparsers.add_parser("graph-rebuild")
    rebuild.add_argument("--db", required=True)
    rebuild.add_argument("--project-id", required=True)

    export = subparsers.add_parser("export")
    export.add_argument("--db", required=True)
    export.add_argument("--project-id", required=True)
    export.add_argument("--out", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    try:
        if args.command == "init":
            version = CanonicalStore(Path(args.db)).init_project(args.project_id, args.title)
            print(json.dumps({"project_id": args.project_id, "version": version}, ensure_ascii=False))
            return 0
        if args.command == "audit":
            store = None
            if args.packet:
                packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
                if args.db and args.project_id:
                    store = CanonicalStore(Path(args.db))
            elif args.db and args.project_id:
                store = CanonicalStore(Path(args.db))
                _, packet = store._load_packet(args.project_id)
            else:
                raise ValidationError("audit needs --packet or --db plus --project-id", "INVALID_AUDIT_ARGS")
            report = audit_packet(packet)
            if store is not None:
                _append_graph_health(report, store.pending_changes(args.project_id), args.project_id)
            print(json.dumps(report.as_dict(), ensure_ascii=False))
            return 0 if report.ok else 2

        store = CanonicalStore(Path(args.db))
        if args.command == "apply":
            packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
            result = store.apply_packet(args.project_id, packet, args.expected_version, args.message)
            print(json.dumps({"project_id": result.project_id, "version": result.version, "snapshot_hash": result.snapshot_hash, "outbox_count": result.outbox_count}, ensure_ascii=False))
            return 0
        if args.command == "context":
            _, packet = store._load_packet(args.project_id)
            print(json.dumps(build_context_with_graph(packet, args.project_id, args.anchor, args.max_hops, args.source), ensure_ascii=False))
            return 0
        if args.command == "graph-sync":
            changes = store.pending_changes(args.project_id)
            projector = GraphProjector()
            try:
                result = projector.sync(args.project_id, changes)
            except ValidationError as error:
                ids = [int(change["change_id"]) for change in changes]
                store.mark_projection(ids, "DEGRADED", str(error))
                raise
            store.mark_projection([int(change["change_id"]) for change in changes], "APPLIED")
            print(json.dumps({"applied": result.applied, "degraded": result.degraded}, ensure_ascii=False))
            return 0
        if args.command == "graph-rebuild":
            count = store.rebuild_changes(args.project_id)
            changes = store.pending_changes(args.project_id)
            projector = GraphProjector()
            try:
                result = projector.rebuild(args.project_id, changes)
            except ValidationError as error:
                ids = [int(change["change_id"]) for change in changes]
                store.mark_projection(ids, "DEGRADED", str(error))
                raise
            store.mark_projection([int(change["change_id"]) for change in changes], "APPLIED")
            print(json.dumps({"queued": count, "applied": result.applied, "degraded": result.degraded}, ensure_ascii=False))
            return 0
        if args.command == "export":
            store.export_markdown(args.project_id, Path(args.out))
            audit_path = Path(args.out).with_name("audit-report.md")
            store.export_audit(args.project_id, audit_path)
            print(json.dumps({"outline": str(args.out), "audit": str(audit_path)}, ensure_ascii=False))
            return 0
        raise ValidationError(f"unknown command: {args.command}", "UNKNOWN_COMMAND")
    except (ValidationError, OSError, json.JSONDecodeError) as error:
        payload = {"error": getattr(error, "code", "RUNTIME_ERROR"), "message": str(error)}
        print(json.dumps(payload, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
