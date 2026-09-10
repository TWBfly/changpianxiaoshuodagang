import json
import os
from copy import deepcopy
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import outline_agent

from outline_agent import (
    CanonicalStore,
    GraphProjector,
    ValidationError,
    audit_packet,
    build_context_from_packet,
    build_context_with_graph,
    main,
    render_packet_markdown,
)


def build_demo_packet():
    return {
        "entities": [
            {"id": "CHAR.a", "kind": "CHARACTER", "namespace": "CANON", "name": "沈砚", "payload": {
                "identity": "县令", "desires": ["保住县城"], "goals": ["查粮案"], "interests": ["民生"],
                "constraints": ["权限不足"], "preferred_strategy": "谈判", "provenance_refs": ["USER.1"],
            }},
            {"id": "CHAR.b", "kind": "CHARACTER", "namespace": "CANON", "name": "顾青禾", "payload": {
                "identity": "粮商", "desires": ["保住商路"], "goals": ["找回账册"], "interests": ["信誉"],
                "constraints": ["被监视"], "preferred_strategy": "交换", "provenance_refs": ["USER.1"],
            }},
            {"id": "PROP.burned-ledger", "kind": "OBJECT", "namespace": "CANON", "name": "烧毁的账册", "payload": {
                "provenance_refs": ["USER.1"],
            }},
            {"id": "LOC.gate", "kind": "LOCATION", "namespace": "CANON", "name": "南城门", "payload": {
                "provenance_refs": ["USER.1"],
            }},
            {"id": "EVENT.1", "kind": "EVENT", "namespace": "PLAN", "name": "封门查粮", "payload": {
                "active_actor": "CHAR.a", "requires_hyperedge": True, "provenance_refs": ["USER.1"],
                "causal_inputs": ["PROP.burned-ledger"], "causal_outputs": ["EVENT.2"],
                "action": "封门并清点粮车", "state_delta": "顾青禾被迫改变账册转移路径",
            }},
            {"id": "EVENT.2", "kind": "EVENT", "namespace": "PLAN", "name": "转移残页", "payload": {
                "active_actor": "CHAR.b", "provenance_refs": ["USER.1"],
                "causal_inputs": ["EVENT.1"], "causal_outputs": ["PROP.burned-ledger"],
                "action": "把账册残页交给可信车夫", "state_delta": "账册证据暂时脱离官府控制",
            }},
        ],
        "edges": [
            {"id": "EDGE.p1", "type": "PARTICIPATES_IN", "source": "CHAR.a", "target": "EVENT.1", "namespace": "PLAN", "payload": {"role": "initiator"}},
            {"id": "EDGE.p2", "type": "PARTICIPATES_IN", "source": "CHAR.b", "target": "EVENT.1", "namespace": "PLAN", "payload": {"role": "target"}},
            {"id": "EDGE.p3", "type": "PARTICIPATES_IN", "source": "PROP.burned-ledger", "target": "EVENT.1", "namespace": "PLAN", "payload": {"role": "evidence"}},
            {"id": "EDGE.p4", "type": "PARTICIPATES_IN", "source": "LOC.gate", "target": "EVENT.1", "namespace": "PLAN", "payload": {"role": "location"}},
            {"id": "EDGE.p5", "type": "PARTICIPATES_IN", "source": "CHAR.b", "target": "EVENT.2", "namespace": "PLAN", "payload": {"role": "initiator"}},
            {"id": "EDGE.c1", "type": "CAUSES", "source": "EVENT.1", "target": "EVENT.2", "namespace": "PLAN", "payload": {}},
        ],
        "negative_facts": ["PROP.burned-ledger"],
    }


def build_chapter_payload(stageable_roles=None):
    roles = stageable_roles or ["ACTION", "COUNTERMOVE", "REPLAN", "COST"]
    beats = []
    for index, role in enumerate(roles, 1):
        beats.append({
            "beat_id": f"BEAT.{index}",
            "beat_role": role,
            "cause_from_previous": f"前一节迫使第{index}步发生",
            "active_actor": "CHAR.a",
            "actor_goal_before": "保住证据",
            "action": f"执行第{index}个主动动作",
            "counterforce": f"对手针对第{index}步反制",
            "what_becomes_impossible_or_more_expensive": "继续原方案的代价上升",
            "new_information_or_choice": f"第{index}步带来新选择",
            "delta": {"goal": f"目标状态变化{index}", "risk": "风险上升"},
            "actor_goal_after": "改用更危险的方案",
            "next_pressure_created": "下一步压力增加",
            "stageability": "STAGEABLE_CORE",
        })
    clusters = [
        {
            "cluster_id": "CLUSTER.1",
            "local_goal": "试探第一条路",
            "active_actors": ["CHAR.a"],
            "conflict_medium": "封锁",
            "stageable_beats": ["BEAT.1", "BEAT.2"],
            "local_turn": "第一条路失败",
            "local_cost": "暴露位置",
            "exit_state": "主角被迫改策",
            "pressure_handed_to_next_cluster": "对手提前设防",
        },
        {
            "cluster_id": "CLUSTER.2",
            "local_goal": "换代价拿到证据",
            "active_actors": ["CHAR.a"],
            "conflict_medium": "交易",
            "stageable_beats": ["BEAT.3", "BEAT.4"],
            "local_turn": "证据只拿到一半",
            "local_cost": "失去安全退路",
            "exit_state": "证据到手但被追踪",
            "pressure_handed_to_next_cluster": "追兵进入下一章",
        },
    ]
    scenes = [
        {
            "scene_id": "SCENE.1",
            "entry_state": "证据尚未暴露",
            "active_actor_goal": "试探封锁缺口",
            "opposing_goal_or_process": "对手维持封锁",
            "immediate_stakes": "证据和身份都会暴露",
            "live_actions": ["试探", "反制"],
            "turn_or_reprice": "退路变贵",
            "exit_state": "第一条方案失败",
            "delta_dimensions": ["risk", "available_path"],
            "payload_cluster_refs": ["CLUSTER.1"],
        },
        {
            "scene_id": "SCENE.2",
            "entry_state": "第一条方案失败",
            "active_actor_goal": "用代价交换证据",
            "opposing_goal_or_process": "对手提出交换条件",
            "immediate_stakes": "拿证据就失去安全退路",
            "live_actions": ["谈判", "换策"],
            "turn_or_reprice": "关系和资源重新定价",
            "exit_state": "证据到手但追兵出现",
            "delta_dimensions": ["knowledge", "resource", "risk"],
            "payload_cluster_refs": ["CLUSTER.2"],
        },
    ]
    return {
        "chapter_no": 1,
        "volume_ref": "VOLUME.1",
        "target_prose_contract": {
            "unit": "CHINESE_PROSE_CHARACTERS",
            "target_min": 4000,
            "target_default": 5000,
            "target_max": 6000,
            "chapter_mode": "STANDARD_LONG",
        },
        "chapter_function": "让主角第一次付出不可逆代价换取证据",
        "core_delta": "证据到手，安全退路消失",
        "conflict_contract": {
            "actor_a": "CHAR.a",
            "actor_b": "CHAR.b",
            "concrete_incompatibility": "证据与安全退路不能同时保全",
        },
        "dynamic_beats": beats,
        "payload_clusters": clusters,
        "line_clusters": ["CLUSTER.1", "CLUSTER.2"],
        "scene_payloads": scenes,
        "explicit_compression": {
            "process_to_summarize": ["普通赶路"],
            "ledger_not_to_itemize": ["库存流水"],
        },
        "continuation_source": "追兵已锁定主角的撤离方向",
        "forbidden_drift": ["不得新增决定性证据"],
        "provenance_refs": ["USER.1"],
        "plan_level": "PRODUCTION_READY",
        "expansion_status": "FULL",
        "mid_chapter_load": "PASS",
        "anti_self_certification": True,
    }


def chapter_entity(payload=None):
    return {
        "id": "CHAPTER.1",
        "kind": "CHAPTER_PLAN",
        "namespace": "PLAN",
        "name": "第一章",
        "payload": payload or build_chapter_payload(),
    }


def build_full_book_packet(expected_chapters=1, chapter_numbers=None):
    chapter_numbers = chapter_numbers or list(range(1, expected_chapters + 1))
    entities = [
        {
            "id": "CHAR.a",
            "kind": "CHARACTER",
            "namespace": "PLAN",
            "name": "沈砚",
            "payload": {
                "identity": "调查员", "desires": ["查清旧案"], "goals": ["保住证据"],
                "interests": ["真相"], "constraints": ["权限不足"], "preferred_strategy": "交换",
                "character_tier": "SUPPORT", "provenance_refs": ["USER.1"],
            },
        },
        {
            "id": "CHAR.b",
            "kind": "CHARACTER",
            "namespace": "PLAN",
            "name": "顾青禾",
            "payload": {
                "identity": "档案员", "desires": ["保住家人"], "goals": ["公开档案"],
                "interests": ["社区"], "constraints": ["被追踪"], "preferred_strategy": "谈判",
                "character_tier": "SUPPORT", "provenance_refs": ["USER.1"],
            },
        },
        {
            "id": "PROJECT.full",
            "kind": "PROJECT",
            "namespace": "CONTRACT",
            "name": "完整长篇项目",
            "payload": {
                "one_sentence_synopsis": "一个被旧案追杀的归来者必须在夺回真相和拆掉个人权力之间作出选择。",
                "causal_summary": "旧案制造归来者，归来者揭开利益链，利益链逼出制度选择，终局以公开审计结算。",
                "provenance_refs": ["USER.1"],
            },
        },
        {
            "id": "VOLUME.1",
            "kind": "VOLUME",
            "namespace": "PLAN",
            "name": "第一卷",
            "payload": {
                "chapter_start": 1,
                "chapter_end": expected_chapters,
                "detailed_plot": "主角回到旧城，在一场产权与证据争夺中建立第一组盟友，并发现旧案不是单一反派造成。",
                "central_conflict": "主角要保住证据与普通人的安全，对手要用合法程序销毁证据。",
                "turning_points": ["归来暴露", "盟友倒戈", "旧案反转", "进入下一地图"],
                "payoff": "第一段责任链公开，主角失去旧身份但取得下一地图的合法入口。",
                "next_hook": "下一卷的控制系统在港口重新启动。",
                "provenance_refs": ["USER.1"],
            },
        },
    ]
    for number in chapter_numbers:
        payload = deepcopy(build_chapter_payload(["ACTION", "COUNTERMOVE", "REPLAN", "COST", "REVELATION", "HOOK"]))
        for index, beat in enumerate(payload["dynamic_beats"], 1):
            beat["active_actor"] = "CHAR.a" if index % 2 else "CHAR.b"
            beat["delta"] = {"knowledge": f"信息变化{index}"} if index % 2 else {"resource": f"资源变化{index}"}
        payload["chapter_no"] = number
        payload["volume_ref"] = "VOLUME.1"
        payload["chapter_function"] = f"第{number}章让主角用新选择换取下一条信息"
        payload["core_delta"] = f"第{number}章的证据、关系和退路发生不可逆变化"
        payload["provenance_refs"] = ["USER.1"]
        payload["payload_clusters"].append({
            "cluster_id": f"CLUSTER.{number}.3",
            "local_goal": "把局部线索转成下一步行动",
            "active_actors": ["CHAR.a", "CHAR.b"],
            "conflict_medium": "公开记录与追捕",
            "stageable_beats": ["BEAT.5", "BEAT.6"],
            "local_turn": "线索反过来指向新的责任人",
            "local_cost": "关系信任下降",
            "exit_state": "获得下一章的行动入口",
            "pressure_handed_to_next_cluster": "对手提前改变路线",
        })
        payload["scene_payloads"].append({
            "scene_id": f"SCENE.{number}.3",
            "entry_state": "第二条方案已经失败",
            "active_actor_goal": "把线索交给可以验证的人",
            "opposing_goal_or_process": "对手切断公开记录",
            "immediate_stakes": "证据和盟友同时可能失去",
            "live_actions": ["转移", "核验", "反制"],
            "turn_or_reprice": "主角必须放弃一项资源",
            "exit_state": "下一张地图被打开",
            "delta_dimensions": ["knowledge", "relationship", "path"],
            "payload_cluster_refs": [f"CLUSTER.{number}.3"],
        })
        entities.append({
            "id": f"CHAPTER.{number}",
            "kind": "CHAPTER_PLAN",
            "namespace": "PLAN",
            "name": f"第{number}章",
            "payload": payload,
        })
    return {
        "entities": entities,
        "edges": [],
        "precision": {
            "production_stage": "FINAL_FULL_BOOK",
            "full_book_detailed_required": True,
            "expected_volumes": 1,
            "expected_chapters": expected_chapters,
        },
    }


class CanonicalStoreTests(unittest.TestCase):
    def test_init_creates_version_zero_and_empty_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            self.assertEqual(store.init_project("PROJECT.demo", "Demo"), 0)
            self.assertEqual(store.get_version("PROJECT.demo"), 0)


class FullBookContractTests(unittest.TestCase):
    def test_final_full_book_cannot_disable_full_detail_gate(self):
        packet = build_full_book_packet(expected_chapters=2, chapter_numbers=[1])
        packet["precision"]["full_book_detailed_required"] = False
        report = audit_packet(packet)
        codes = {item["code"] for item in report.errors}
        self.assertIn("FULL_BOOK_MODE_REQUIRED", codes)

    def test_full_book_requires_synopsis_scope_and_volume_details(self):
        packet = build_full_book_packet(expected_chapters=2, chapter_numbers=[1, 2])
        project = next(entity for entity in packet["entities"] if entity["kind"] == "PROJECT")
        project["payload"].pop("one_sentence_synopsis")
        report = audit_packet(packet)
        self.assertIn("PROJECT_SYNOPSIS_MISSING", {item["code"] for item in report.errors})

    def test_full_book_rejects_thin_long_chapter(self):
        packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
        chapter = next(entity for entity in packet["entities"] if entity["kind"] == "CHAPTER_PLAN")
        chapter["payload"]["dynamic_beats"] = chapter["payload"]["dynamic_beats"][:4]
        report = audit_packet(packet)
        self.assertIn("CHAPTER_PAYLOAD_SHORTFALL", {item["code"] for item in report.errors})

    def test_final_full_book_rejects_prose_range_outside_policy(self):
        packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
        contract = next(entity for entity in packet["entities"] if entity["kind"] == "CHAPTER_PLAN")["payload"]["target_prose_contract"]
        contract.update({"target_min": 1, "target_max": 99999})
        report = audit_packet(packet)
        self.assertIn("TARGET_PROSE_RANGE_OUT_OF_POLICY", {item["code"] for item in report.errors})

    def test_final_full_book_rejects_unknown_volume_reference(self):
        packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
        chapter = next(entity for entity in packet["entities"] if entity["kind"] == "CHAPTER_PLAN")
        chapter["payload"]["volume_ref"] = "VOLUME.missing"
        report = audit_packet(packet)
        self.assertIn("CHAPTER_VOLUME_REFERENCE_INVALID", {item["code"] for item in report.errors})

    def test_final_full_book_rejects_incomplete_beat_and_scene_coverage(self):
        packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
        chapter = next(entity for entity in packet["entities"] if entity["kind"] == "CHAPTER_PLAN")["payload"]
        chapter["payload_clusters"][0]["stageable_beats"] = []
        chapter["scene_payloads"][2]["payload_cluster_refs"] = ["CLUSTER.1"]
        report = audit_packet(packet)
        codes = {item["code"] for item in report.errors}
        self.assertIn("CHAPTER_BEAT_CLUSTER_COVERAGE", codes)
        self.assertIn("CHAPTER_SCENE_CLUSTER_COVERAGE", codes)

    def test_final_full_book_rejects_duplicate_core_beat_delta(self):
        packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
        chapter = next(entity for entity in packet["entities"] if entity["kind"] == "CHAPTER_PLAN")["payload"]
        chapter["dynamic_beats"][1]["delta"] = deepcopy(chapter["dynamic_beats"][0]["delta"])
        report = audit_packet(packet)
        self.assertIn("CHAPTER_DUPLICATE_DELTA", {item["code"] for item in report.errors})

    def test_malformed_final_entities_return_audit_error(self):
        packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
        packet["entities"].append(None)
        report = audit_packet(packet)
        self.assertIn("INVALID_ENTITY", {item["code"] for item in report.errors})

    def test_final_full_book_rejects_invalid_project_text_and_actor_reference(self):
        packet = build_full_book_packet(expected_chapters=1, chapter_numbers=[1])
        project = next(entity for entity in packet["entities"] if entity["kind"] == "PROJECT")
        project["payload"]["one_sentence_synopsis"] = 42
        chapter = next(entity for entity in packet["entities"] if entity["kind"] == "CHAPTER_PLAN")
        chapter["payload"]["dynamic_beats"][0]["active_actor"] = "CHAR.missing"
        report = audit_packet(packet)
        codes = {item["code"] for item in report.errors}
        self.assertIn("PROJECT_SYNOPSIS_INVALID", codes)
        self.assertIn("CHAPTER_ACTOR_REFERENCE_INVALID", codes)

    def test_export_has_synopsis_volume_index_then_detailed_chapters(self):
        text = render_packet_markdown(build_full_book_packet(expected_chapters=2, chapter_numbers=[1, 2]))
        self.assertLess(text.index("全书一句话总纲"), text.index("卷级详细剧情"))
        self.assertLess(text.index("卷级详细剧情"), text.index("全章目录与推进表"))
        self.assertLess(text.index("全章目录与推进表"), text.index("指定窗口详细章纲"))

    def test_stale_expected_version_is_rejected_without_partial_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            packet = {"entities": [{"id": "RULE.a", "kind": "RULE", "name": "雨季", "payload": {"provenance_refs": ["USER.1"]}}], "edges": []}
            store.apply_packet("PROJECT.demo", packet, 0, "first")
            with self.assertRaises(ValidationError):
                store.apply_packet("PROJECT.demo", packet, 0, "stale")
            self.assertEqual(store.get_version("PROJECT.demo"), 1)

    def test_snapshot_removes_entities_and_edges_omitted_by_next_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            first = {
                "entities": [
                    {"id": "CHAR.a", "kind": "CHARACTER", "name": "沈砚", "payload": {
                        "identity": "县令", "desires": ["查案"], "goals": ["查案"],
                        "interests": ["民生"], "constraints": ["权限"],
                        "preferred_strategy": "谈判", "provenance_refs": ["USER.1"],
                    }},
                    {"id": "EVENT.1", "kind": "EVENT", "name": "封门", "payload": {
                        "active_actor": "CHAR.a", "provenance_refs": ["USER.1"],
                        "causal_inputs": ["CHAR.a"], "causal_outputs": ["CHAR.a"],
                        "action": "封门", "state_delta": "通行受限",
                    }},
                ],
                "edges": [{"id": "EDGE.a", "type": "PARTICIPATES_IN", "source": "CHAR.a", "target": "EVENT.1", "payload": {}}],
            }
            store.apply_packet("PROJECT.demo", first, 0, "first")
            store.apply_packet("PROJECT.demo", {"entities": [], "edges": []}, 1, "replace")
            _, loaded = store._load_packet("PROJECT.demo")
            self.assertEqual(loaded["entities"], [])
            self.assertEqual(loaded["edges"], [])
            pending = store.pending_changes("PROJECT.demo")
            self.assertTrue(any(row["action"] == "DELETE" for row in pending))

    def test_patch_mode_overlays_without_deleting_omitted_entities(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            store.apply_packet("PROJECT.demo", {"entities": [{"id": "RULE.a", "kind": "RULE", "name": "雨季", "payload": {"provenance_refs": ["USER.1"]}}], "edges": []}, 0, "first")
            store.apply_packet("PROJECT.demo", {"packet_mode": "PATCH", "entities": [{"id": "RULE.b", "kind": "RULE", "name": "旱季", "payload": {"provenance_refs": ["USER.1"]}}], "edges": []}, 1, "patch")
            _, loaded = store._load_packet("PROJECT.demo")
            self.assertEqual([item["id"] for item in loaded["entities"]], ["RULE.a", "RULE.b"])

    def test_patch_rejects_unhashable_negative_fact_at_input_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            with self.assertRaises(ValidationError) as context:
                store.apply_packet("PROJECT.demo", {"packet_mode": "PATCH", "entities": [], "edges": [], "negative_facts": [{}]}, 0, "bad")
            self.assertEqual(context.exception.code, "INVALID_PACKET")

    def test_identical_snapshot_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            packet = {"entities": [{"id": "RULE.a", "kind": "RULE", "name": "雨季", "payload": {"provenance_refs": ["USER.1"]}}], "edges": []}
            first = store.apply_packet("PROJECT.demo", packet, 0, "first")
            second = store.apply_packet("PROJECT.demo", packet, 1, "retry")
            self.assertEqual(second.version, first.version)
            self.assertEqual(store.get_version("PROJECT.demo"), 1)

    def test_rebuild_changes_requeues_current_canon_without_version_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            store.apply_packet("PROJECT.demo", {"entities": [{"id": "RULE.a", "kind": "RULE", "name": "雨季", "payload": {"provenance_refs": ["USER.1"]}}], "edges": []}, 0, "first")
            with store._connect() as connection:
                ids = [row["change_id"] for row in connection.execute("SELECT change_id FROM changes").fetchall()]
            store.mark_projection(ids, "APPLIED")
            self.assertEqual(store.rebuild_changes("PROJECT.demo"), 1)
            self.assertEqual(store.get_version("PROJECT.demo"), 1)
            self.assertEqual(len(store.pending_changes("PROJECT.demo")), 1)

    def test_commit_history_can_reconstruct_an_older_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            packet = {"entities": [{"id": "RULE.a", "kind": "RULE", "name": "雨季", "payload": {"provenance_refs": ["USER.1"]}}], "edges": []}
            store.apply_packet("PROJECT.demo", packet, 0, "first")
            store.apply_packet("PROJECT.demo", {"entities": [], "edges": []}, 1, "remove")
            self.assertEqual(store.load_snapshot("PROJECT.demo", 1)["entities"][0]["id"], "RULE.a")

    def test_unnamed_actor_and_missing_agency_are_hard_errors(self):
        packet = {
            "entities": [{
                "id": "CHAR.bad", "kind": "CHARACTER", "namespace": "CANON",
                "name": "路人甲", "payload": {"identity": "护卫"},
            }],
            "edges": [],
        }
        report = audit_packet(packet)
        self.assertFalse(report.ok)
        codes = {item["code"] for item in report.errors}
        self.assertIn("PLACEHOLDER_PERSON", codes)
        self.assertIn("CHARACTER_WITHOUT_AGENCY", codes)

    def test_core_character_requires_lived_experience_and_decision_model(self):
        packet = {"entities": [{"id": "CHAR.core", "kind": "CHARACTER", "name": "林照", "payload": {
            "character_tier": "CORE", "identity": "药铺掌柜", "desires": ["保住药铺"],
            "goals": ["找出断供原因"], "interests": ["伙计生计"], "constraints": ["欠债"],
            "preferred_strategy": "算账", "provenance_refs": ["USER.1"],
        }}], "edges": []}
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("CHARACTER_LIFE_PROFILE_MISSING", codes)

    def test_event_event_causal_fields_need_matching_causal_edges(self):
        packet = build_demo_packet()
        event = next(item for item in packet["entities"] if item["id"] == "EVENT.1")
        event["payload"]["causal_outputs"] = ["EVENT.2"]
        packet["edges"] = [edge for edge in packet["edges"] if edge["id"] != "EDGE.c1"]
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("CAUSAL_OUTPUT_EDGE_MISSING", codes)

    def test_production_ready_chapter_needs_real_capacity_evidence(self):
        packet = {"entities": [{"id": "CHAPTER.1", "kind": "CHAPTER_PLAN", "name": "第一章", "payload": {
            "plan_level": "PRODUCTION_READY", "provenance_refs": ["USER.1"],
            "dynamic_beats": ["beat-1"], "line_clusters": ["LINE.a"], "scene_payloads": ["scene-1"],
            "expansion_status": "PARTIAL", "mid_chapter_load": "PASS", "anti_self_certification": True,
        }}], "edges": []}
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("CAPACITY_GATE_FAILED", codes)

    def test_result_only_chapter_cannot_pass_capacity_audit(self):
        payload = build_chapter_payload()
        payload["dynamic_beats"] = [{"stageability": "RESULT_ONLY", "action": "他改变了主意"}]
        report = audit_packet({"entities": [chapter_entity(payload)], "edges": []})
        self.assertIn("CAPACITY_GATE_FAILED", {item["code"] for item in report.errors})

    def test_middle_empty_chapter_cannot_pass_capacity_audit(self):
        payload = build_chapter_payload(["ACTION", "COUNTERMOVE", "ACTION", "COUNTERMOVE"])
        report = audit_packet({"entities": [chapter_entity(payload)], "edges": []})
        errors = {item["code"] for item in report.errors}
        self.assertIn("CAPACITY_GATE_FAILED", errors)
        capacity_fn = getattr(outline_agent, "audit_chapter_capacity", None)
        self.assertIsNotNone(capacity_fn)
        if capacity_fn is None:
            return
        capacity = capacity_fn(chapter_entity(payload))
        self.assertIn("MID_CHAPTER_LOAD_FAILED", capacity["failure_reasons"])

    def test_structured_long_chapter_passes_independent_capacity_audit(self):
        capacity_fn = getattr(outline_agent, "audit_chapter_capacity", None)
        self.assertIsNotNone(capacity_fn)
        if capacity_fn is None:
            return
        result = capacity_fn(chapter_entity())
        self.assertEqual(result["final_capacity"], "FULL")
        self.assertEqual(result["stageable_core_beats"], 4)
        self.assertEqual(result["payload_clusters"], 2)
        self.assertEqual(result["core_scenes"], 2)

    def test_unknown_chapter_mode_cannot_bypass_long_capacity(self):
        payload = build_chapter_payload()
        payload["target_prose_contract"]["chapter_mode"] = "UNKNOWN"
        payload["payload_clusters"] = payload["payload_clusters"][:1]
        payload["scene_payloads"] = payload["scene_payloads"][:1]
        report = audit_packet({"entities": [chapter_entity(payload)], "edges": []})
        self.assertIn("CAPACITY_GATE_FAILED", {item["code"] for item in report.errors})

    def test_full_book_mode_rejects_missing_chapter_plan(self):
        packet = {
            "entities": [{
                "id": "VOLUME.1", "kind": "VOLUME", "name": "第一卷",
                "payload": {"provenance_refs": ["USER.1"]},
            }],
            "edges": [],
            "precision": {"full_book_detailed_required": True, "expected_chapters": 1},
        }
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("CHAPTER_PLAN_MISSING", codes)

    def test_full_book_mode_requires_expected_chapter_count(self):
        packet = {
            "entities": [chapter_entity()],
            "edges": [],
            "precision": {"full_book_detailed_required": True},
        }
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("EXPECTED_CHAPTERS_REQUIRED", codes)

    def test_full_book_mode_handles_invalid_chapter_payload_without_crashing(self):
        packet = {
            "entities": [{"id": "CHAPTER.1", "kind": "CHAPTER_PLAN", "name": "坏章", "payload": "not-an-object"}],
            "edges": [],
            "precision": {"full_book_detailed_required": True, "expected_chapters": 1},
        }
        report = audit_packet(packet)
        self.assertIn("INVALID_PAYLOAD", {item["code"] for item in report.errors})

    def test_full_book_mode_rejects_index_only_chapter(self):
        payload = build_chapter_payload()
        payload["plan_level"] = "STORY_NODE"
        packet = {
            "entities": [chapter_entity(payload)],
            "edges": [],
            "precision": {"full_book_detailed_required": True, "expected_chapters": 1},
        }
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("CHAPTER_NOT_PRODUCTION_READY", codes)

    def test_full_book_mode_accepts_one_complete_production_ready_chapter(self):
        packet = {
            "entities": [chapter_entity()],
            "edges": [],
            "precision": {"full_book_detailed_required": True, "expected_chapters": 1},
        }
        self.assertTrue(audit_packet(packet).ok)

    def test_missing_context_anchor_returns_insufficient_instead_of_crashing(self):
        context = build_context_from_packet({"entities": [], "edges": []}, ["CHAR.missing"])
        self.assertEqual(context["retrieval_sufficiency"], "INSUFFICIENT")
        self.assertIn("anchors", context["missing"])

    def test_edge_payload_must_be_an_object(self):
        packet = build_demo_packet()
        packet["edges"][0]["payload"] = []
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("INVALID_PAYLOAD", codes)

    def test_unknown_namespace_is_rejected(self):
        packet = {"entities": [{
            "id": "RULE.candidate", "kind": "RULE", "namespace": "CANDIDATE",
            "name": "候选规则", "payload": {"provenance_refs": ["USER.1"]},
        }], "edges": []}
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("INVALID_NAMESPACE", codes)

    def test_hyperedge_requires_distinct_participants(self):
        packet = build_demo_packet()
        for edge in packet["edges"]:
            if edge["target"] == "EVENT.1" and edge["type"] == "PARTICIPATES_IN":
                edge["source"] = "CHAR.a"
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("HYPEREDGE_DUPLICATE_PARTICIPANT", codes)

    def test_outbox_only_contains_changed_objects(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            first = {"entities": [
                {"id": "RULE.a", "kind": "RULE", "name": "雨季", "payload": {"provenance_refs": ["USER.1"]}},
                {"id": "RULE.b", "kind": "RULE", "name": "旱季", "payload": {"provenance_refs": ["USER.1"]}},
            ], "edges": []}
            store.apply_packet("PROJECT.demo", first, 0, "first")
            with store._connect() as connection:
                ids = [row["change_id"] for row in connection.execute("SELECT change_id FROM changes")]
            store.mark_projection(ids, "APPLIED")
            changed = {"entities": [
                {"id": "RULE.a", "kind": "RULE", "name": "雨季延长", "payload": {"provenance_refs": ["USER.1"]}},
                first["entities"][1],
            ], "edges": []}
            store.apply_packet("PROJECT.demo", changed, 1, "change one")
            pending = store.pending_changes("PROJECT.demo")
            self.assertEqual({row["object_id"] for row in pending}, {"RULE.a"})

    def test_human_state_requires_body_routine_obligations_and_need(self):
        packet = {"entities": [{"id": "STATE.a", "kind": "HUMAN_STATE", "name": "林照当日状态", "payload": {
            "provenance_refs": ["USER.1"], "bodily_state": "疲惫",
        }}], "edges": []}
        self.assertIn("HUMAN_REALITY_PROFILE_MISSING", {item["code"] for item in audit_packet(packet).errors})

    def test_event_requires_provenance_and_causal_actor(self):
        packet = {
            "entities": [{
                "id": "EVENT.1", "kind": "EVENT", "namespace": "PLAN",
                "name": "突发反转", "payload": {"action": "发生"},
            }],
            "edges": [],
        }
        report = audit_packet(packet)
        self.assertFalse(report.ok)
        codes = {item["code"] for item in report.errors}
        self.assertIn("MISSING_PROVENANCE", codes)
        self.assertIn("ORPHAN_EVENT", codes)

    def test_event_cannot_be_a_result_only_or_reference_missing_entities(self):
        packet = {
            "entities": [{
                "id": "CHAR.a", "kind": "CHARACTER", "namespace": "CANON",
                "name": "沈砚", "payload": {
                    "identity": "县令", "desires": ["查案"], "goals": ["查案"],
                    "interests": ["民生"], "constraints": ["权限"],
                    "preferred_strategy": "查账", "provenance_refs": ["USER.1"],
                },
            }, {
                "id": "EVENT.1", "kind": "EVENT", "namespace": "PLAN",
                "name": "结果句", "payload": {
                    "active_actor": "CHAR.a", "provenance_refs": ["USER.1"],
                    "causal_inputs": ["MISSING.1"], "causal_outputs": ["EVENT.2"],
                },
            }],
            "edges": [],
        }
        codes = {item["code"] for item in audit_packet(packet).errors}
        self.assertIn("EVENT_ACTION_MISSING", codes)
        self.assertIn("BROKEN_REFERENCE", codes)
        self.assertIn("UNLINKED_CAUSAL_ACTOR", codes)

    def test_apply_rejects_invalid_packet_before_version_increment(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            invalid = {
                "entities": [{"id": "CHAR.bad", "kind": "CHARACTER", "name": "路人甲", "payload": {}}],
                "edges": [],
            }
            with self.assertRaises(ValidationError) as context:
                store.apply_packet("PROJECT.demo", invalid, 0, "invalid")
            self.assertEqual(context.exception.code, "PLACEHOLDER_PERSON")
            self.assertEqual(store.get_version("PROJECT.demo"), 0)

    def test_causal_cycle_is_rejected(self):
        base = {
            "provenance_refs": ["USER.1"], "causal_inputs": ["RULE.1"],
            "causal_outputs": ["EVENT.2"], "active_actor": "CHAR.a",
        }
        packet = {
            "entities": [
                {"id": "CHAR.a", "kind": "CHARACTER", "name": "沈砚", "payload": {
                    "identity": "县令", "desires": ["保境"], "goals": ["查案"],
                    "interests": ["民生"], "constraints": ["权限"], "preferred_strategy": "谈判",
                    "provenance_refs": ["USER.1"],
                }},
                {"id": "EVENT.1", "kind": "EVENT", "name": "一", "payload": base},
                {"id": "EVENT.2", "kind": "EVENT", "name": "二", "payload": {
                    **base, "causal_inputs": ["EVENT.1"], "causal_outputs": ["EVENT.1"],
                }},
            ],
            "edges": [
                {"id": "EDGE.1", "type": "CAUSES", "source": "EVENT.1", "target": "EVENT.2"},
                {"id": "EDGE.2", "type": "CAUSES", "source": "EVENT.2", "target": "EVENT.1"},
            ],
        }
        report = audit_packet(packet)
        self.assertIn("CAUSAL_CYCLE", {e["code"] for e in report.errors})


class Neo4jProjectionTests(unittest.TestCase):
    def test_graph_identity_is_scoped_to_project(self):
        constraints = (Path(__file__).parents[1] / "graph" / "constraints.cypher").read_text(encoding="utf-8")
        self.assertIn("(n.project_id, n.id) IS UNIQUE", constraints)

    def test_edge_payload_is_kept_as_json_with_only_safe_top_level_properties(self):
        class FakeProjector(GraphProjector):
            def __init__(self):
                super().__init__(shell="fake")
                self.params = None
            def ensure_schema(self):
                return None
            def _run(self, _cypher, params=None):
                self.params = params
                return ""

        projector = FakeProjector()
        projector.sync("PROJECT.demo", [{
            "change_id": 1, "version": 1, "object_type": "EDGE", "object_id": "EDGE.1",
            "action": "UPSERT", "before_json": None,
            "after_json": json.dumps({
                "edge_id": "EDGE.1", "edge_type": "PARTICIPATES_IN", "source_id": "CHAR.a",
                "target_id": "EVENT.1", "namespace": "PLAN", "status": "ACTIVE",
                "payload_json": json.dumps({"role": "initiator", "unsafe-key": "value"}),
            }),
        }])
        props = projector.params["edges"][0]["props"]
        self.assertEqual(props["role"], "initiator")
        self.assertNotIn("unsafe-key", props)
        self.assertIn("payload", props)

    def test_projector_rejects_edges_with_missing_endpoints_before_projection(self):
        class MissingEndpointProjector(GraphProjector):
            def __init__(self):
                super().__init__(shell="fake")
                self.projection_called = False

            def ensure_schema(self):
                return None

            def _run(self, cypher, params=None):
                if cypher == self.EDGE_PREFLIGHT:
                    return "edge_id\tsource_id\ttarget_id\nEDGE.1\tCHAR.missing\tEVENT.missing\n"
                self.projection_called = True
                return ""

        projector = MissingEndpointProjector()
        with self.assertRaises(ValidationError) as context:
            projector.sync("PROJECT.demo", [{
                "change_id": 1, "version": 1, "object_type": "EDGE", "object_id": "EDGE.1",
                "action": "UPSERT", "before_json": None,
                "after_json": json.dumps({
                    "edge_id": "EDGE.1", "edge_type": "CAUSES", "source_id": "CHAR.missing",
                    "target_id": "EVENT.missing", "namespace": "PLAN", "status": "ACTIVE",
                    "payload_json": "{}",
                }),
            }])
        self.assertEqual(context.exception.code, "NEO4J_ENDPOINT_MISSING")
        self.assertFalse(projector.projection_called)

    def test_projector_requires_local_shell_configuration(self):
        projector = GraphProjector(shell="/missing/cypher-shell")
        with self.assertRaises(ValidationError) as context:
            projector.ensure_schema()
        self.assertEqual(context.exception.code, "NEO4J_SHELL_NOT_FOUND")

    def test_projector_bounds_a_stalled_shell(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "cypher-shell"
            fake.write_text("#!/bin/sh\nsleep 2\n", encoding="utf-8")
            fake.chmod(0o755)
            old_user = os.environ.get("NEO4J_USERNAME")
            old_password = os.environ.get("NEO4J_PASSWORD")
            os.environ["NEO4J_USERNAME"] = "test"
            os.environ["NEO4J_PASSWORD"] = "test"
            try:
                projector = GraphProjector(shell=str(fake), timeout_seconds=0.05)
                with self.assertRaises(ValidationError) as context:
                    projector._run("RETURN 1")
                self.assertEqual(context.exception.code, "NEO4J_TIMEOUT")
            finally:
                if old_user is None:
                    os.environ.pop("NEO4J_USERNAME", None)
                else:
                    os.environ["NEO4J_USERNAME"] = old_user
                if old_password is None:
                    os.environ.pop("NEO4J_PASSWORD", None)
                else:
                    os.environ["NEO4J_PASSWORD"] = old_password

    def test_projector_blocks_remote_endpoint_by_default(self):
        projector = GraphProjector(shell="/bin/echo")
        old_user, old_password, old_uri = (os.environ.get(key) for key in ("NEO4J_USERNAME", "NEO4J_PASSWORD", "NEO4J_URI"))
        os.environ["NEO4J_USERNAME"] = "test"
        os.environ["NEO4J_PASSWORD"] = "test"
        os.environ["NEO4J_URI"] = "neo4j://example.invalid:7687"
        try:
            with self.assertRaises(ValidationError) as context:
                projector._run("RETURN 1")
            self.assertEqual(context.exception.code, "NEO4J_REMOTE_BLOCKED")
        finally:
            for key, value in (("NEO4J_USERNAME", old_user), ("NEO4J_PASSWORD", old_password), ("NEO4J_URI", old_uri)):
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_query_rejects_non_allowlisted_script(self):
        projector = GraphProjector(shell="/missing/cypher-shell")
        with self.assertRaises(ValidationError) as context:
            projector.query("DROP ALL", {})
        self.assertEqual(context.exception.code, "QUERY_NOT_ALLOWED")

    def test_sync_translates_delete_changes_without_reading_empty_after_json(self):
        class FakeProjector(GraphProjector):
            def __init__(self):
                super().__init__(shell="fake")
                self.params = None
            def ensure_schema(self):
                return None
            def _run(self, _cypher, params=None):
                self.params = params
                return ""

        projector = FakeProjector()
        result = projector.sync("PROJECT.demo", [{
            "change_id": 1, "version": 2, "object_type": "ENTITY", "object_id": "CHAR.a",
            "action": "DELETE", "before_json": json.dumps({"entity_id": "CHAR.a"}), "after_json": "{}",
        }])
        self.assertEqual(result.applied, 1)
        self.assertEqual(projector.params["delete_entities"], [{"id": "CHAR.a"}])

    def test_allowlisted_queries_are_project_scoped(self):
        projector = GraphProjector(shell="/missing/cypher-shell")
        self.assertIn("project_id", projector.query_text("character_neighborhood"))
        self.assertIn("project_id", projector.query_text("causal_path"))
        self.assertIn("project_id", projector.query_text("hyperedge_context"))


class ContextPacketTests(unittest.TestCase):
    def test_context_packet_keeps_hyperedge_roles_and_negative_facts(self):
        context = build_context_from_packet(build_demo_packet(), ["CHAR.a"], max_hops=2)
        self.assertEqual(context["retrieval_sufficiency"], "SUFFICIENT")
        self.assertEqual(context["hyperedges"][0]["participants"][0]["role"], "initiator")
        self.assertIn("PROP.burned-ledger", context["negative_facts"])

    def test_canon_round_trip_preserves_negative_facts(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            store.apply_packet("PROJECT.demo", build_demo_packet(), 0, "demo")
            _, packet = store._load_packet("PROJECT.demo")
            self.assertEqual(packet["negative_facts"], ["PROP.burned-ledger"])

    def test_canon_round_trip_preserves_packet_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            packet = build_demo_packet()
            packet.update({
                "assumptions": ["故事发生在旱灾后的第三年"],
                "open_questions": ["上级买家是否会在下一卷现身"],
                "source_refs": ["USER.brief", "PDF.graph-memory"],
                "precision": {"time": "ordered", "space": "coarse"},
            })
            store.apply_packet("PROJECT.demo", packet, 0, "demo")
            _, loaded = store._load_packet("PROJECT.demo")
            self.assertEqual(loaded["assumptions"], packet["assumptions"])
            self.assertEqual(loaded["open_questions"], packet["open_questions"])
            self.assertEqual(loaded["source_refs"], packet["source_refs"])
            self.assertEqual(loaded["precision"], packet["precision"])

    def test_context_timeline_is_sorted_and_case_normalized(self):
        packet = build_demo_packet()
        by_id = {item["id"]: item for item in packet["entities"]}
        by_id["EVENT.1"]["payload"]["time_index"] = 2
        by_id["EVENT.2"]["payload"]["time_index"] = 1
        context = build_context_from_packet(packet, ["CHAR.a"], max_hops=3)
        self.assertEqual([item["id"] for item in context["timeline_facts"]], ["EVENT.2", "EVENT.1"])
        self.assertEqual({edge["id"] for edge in context["causal_paths"]}, {"EDGE.c1"})

    def test_auto_graph_context_degrades_to_sqlite_explicitly(self):
        class MissingGraph:
            def query(self, *_args, **_kwargs):
                raise ValidationError("credentials missing", "NEO4J_CONFIG_MISSING")

        context = build_context_with_graph(build_demo_packet(), "PROJECT.demo", ["CHAR.a"], projector=MissingGraph())
        self.assertEqual(context["retrieval_source"], "SQLITE")
        self.assertEqual(context["graph_status"]["code"], "NEO4J_CONFIG_MISSING")


class ExportTests(unittest.TestCase):
    def test_export_is_stable_and_contains_required_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            store.apply_packet("PROJECT.demo", build_demo_packet(), 0, "demo")
            first = Path(tmp) / "one.md"
            second = Path(tmp) / "two.md"
            store.export_markdown("PROJECT.demo", first)
            store.export_markdown("PROJECT.demo", second)
            self.assertEqual(first.read_text(), second.read_text())
            text = first.read_text()
            self.assertIn("# 项目总契约与禁止事项", text)
            self.assertIn("# 全人物总表", text)
            self.assertIn("CHAR.a", text)
            self.assertIn("EVENT.1", text)
            self.assertIn("负事实与禁止漂移", text)
            self.assertIn("PROP.burned-ledger", text)
            self.assertEqual(sum(line.startswith("- `CHAR.") for line in text.splitlines()), 4)

    def test_export_audit_surfaces_degraded_graph_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            store.init_project("PROJECT.demo", "Demo")
            result = store.apply_packet("PROJECT.demo", build_demo_packet(), 0, "demo")
            with store._connect() as connection:
                change_ids = [
                    row["change_id"]
                    for row in connection.execute(
                        "SELECT change_id FROM changes WHERE project_id = ?", ("PROJECT.demo",)
                    ).fetchall()
                ]
            store.mark_projection(change_ids, "DEGRADED", "credentials missing")
            report_path = Path(tmp) / "audit.md"
            store.export_audit("PROJECT.demo", report_path)
            text = report_path.read_text(encoding="utf-8")
            self.assertIn("GRAPH_DEGRADED", text)


class CliTests(unittest.TestCase):
    def test_cli_init_and_apply_emit_machine_readable_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "outline.db")
            packet_path = Path(tmp) / "packet.json"
            packet_path.write_text(json.dumps(build_demo_packet(), ensure_ascii=False), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["init", "--db", db, "--project-id", "PROJECT.demo", "--title", "Demo"]), 0)
                self.assertEqual(main([
                    "apply", "--db", db, "--project-id", "PROJECT.demo", "--expected-version", "0",
                    "--packet", str(packet_path), "--message", "demo",
                ]), 0)
            rows = [json.loads(line) for line in output.getvalue().splitlines()]
            self.assertEqual(rows[0]["version"], 0)
            self.assertEqual(rows[1]["version"], 1)

    def test_cli_rejects_packet_without_entities_and_edges(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "outline.db")
            packet_path = Path(tmp) / "packet.json"
            packet_path.write_text("{}", encoding="utf-8")
            main(["init", "--db", db, "--project-id", "PROJECT.demo", "--title", "Demo"])
            output = StringIO()
            with redirect_stdout(output):
                code = main([
                    "apply", "--db", db, "--project-id", "PROJECT.demo", "--expected-version", "0",
                    "--packet", str(packet_path), "--message", "invalid",
                ])
            self.assertEqual(code, 2)
            self.assertIn("INVALID_PACKET", output.getvalue())

    def test_cli_audit_packet_does_not_require_a_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet_path = Path(tmp) / "packet.json"
            packet_path.write_text(json.dumps({"entities": [], "edges": []}), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                code = main(["audit", "--packet", str(packet_path)])
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(output.getvalue())["ok"])

    def test_cli_audit_packet_can_also_report_graph_health(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = str(Path(tmp) / "outline.db")
            packet_path = Path(tmp) / "packet.json"
            packet_path.write_text(json.dumps({"entities": [], "edges": []}), encoding="utf-8")
            CanonicalStore(Path(db)).init_project("PROJECT.demo", "Demo")
            output = StringIO()
            with redirect_stdout(output):
                code = main([
                    "audit", "--packet", str(packet_path), "--db", db, "--project-id", "PROJECT.demo",
                ])
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(output.getvalue())["ok"])


class DemoTests(unittest.TestCase):
    def test_demo_packet_has_no_hard_errors_and_exports_required_sections(self):
        demo_path = Path(__file__).with_name("demo_packet.json")
        packet = json.loads(demo_path.read_text(encoding="utf-8"))
        report = audit_packet(packet)
        self.assertTrue(report.ok, report.errors)
        self.assertEqual(
            {entity["kind"] for entity in packet["entities"] if entity["kind"] == "CHARACTER"},
            {"CHARACTER"},
        )
        text = render_packet_markdown(packet)
        for heading in ("项目总契约", "全人物总表", "Dynamic N-Line", "全书主因果链", "伏笔"):
            self.assertIn(heading, text)

    def test_demo_export_contains_structured_chapter_capacity_and_stable_roster_ids(self):
        demo_path = Path(__file__).with_name("demo_packet.json")
        packet = json.loads(demo_path.read_text(encoding="utf-8"))
        text = render_packet_markdown(packet)
        self.assertIn("CHAPTER.1", text)
        self.assertIn("capacity_audit", text)
        self.assertIn("`CHAR.shenyan`", text)


class AdversarialRobustnessTests(unittest.TestCase):
    def test_cypher_literal_handles_multiline_newlines_and_quotes(self):
        from outline_agent import _cypher_literal
        sample = "第1行：主角深入敌阵\n第2行：发现'密信'与反斜杠\\内容\r\n第3行：制表符\t测试"
        literal = _cypher_literal(sample)
        self.assertTrue(literal.startswith("'") and literal.endswith("'"))
        self.assertNotIn("\n", literal)
        self.assertNotIn("\r", literal)
        self.assertNotIn("\t", literal)
        self.assertIn("\\n", literal)
        self.assertIn("\\'", literal)
        self.assertIn("\\\\", literal)

    def test_merge_patch_with_negative_facts_override_and_registry_dict_merge(self):
        base = {
            "entities": [{"id": "CHAR.1", "name": "A"}],
            "edges": [],
            "negative_facts": ["FACT.old1", "FACT.old2"],
            "provenance_registry": {"SRC.1": "brief-1", "SRC.2": "brief-2"},
        }
        patch = {
            "entities": [{"id": "CHAR.2", "name": "B"}],
            "negative_facts": ["FACT.new_only"],
            "provenance_registry": {"SRC.2": "brief-2-updated", "SRC.3": "brief-3"},
        }
        merged = CanonicalStore._merge_patch(base, patch)
        self.assertEqual(merged["negative_facts"], ["FACT.new_only"])
        self.assertEqual(merged["provenance_registry"], {
            "SRC.1": "brief-1",
            "SRC.2": "brief-2-updated",
            "SRC.3": "brief-3",
        })
        self.assertEqual(len(merged["entities"]), 2)

    def test_audit_chapter_capacity_with_adaptive_literary_beats(self):
        payload = build_chapter_payload(["ACTION", "COUNTERMOVE", "REPLAN", "COST", "CLIMAX"])
        chapter = {
            "id": "CHAPTER_PLAN.1",
            "kind": "CHAPTER_PLAN",
            "namespace": "PLAN",
            "payload": payload,
        }
        capacity = outline_agent.audit_chapter_capacity(chapter)
        self.assertEqual(capacity["final_capacity"], "FULL")
        self.assertEqual(capacity["mid_chapter_load"], "PASS")

    def test_global_topological_causal_time_inversion_rejected(self):
        packet = {
            "entities": [
                {"id": "CHAR.a", "kind": "CHARACTER", "name": "主角", "payload": {
                    "identity": "修士", "desires": ["复仇"], "goals": ["夺宝"], "interests": ["生机"],
                    "constraints": ["重伤"], "preferred_strategy": "暗杀", "provenance_refs": ["U.1"],
                }},
                {"id": "EVENT.1", "kind": "EVENT", "name": "夺宝事件", "payload": {
                    "active_actor": "CHAR.a", "provenance_refs": ["U.1"], "time_index": 100,
                    "causal_inputs": ["CHAR.a"], "causal_outputs": ["EVENT.2"],
                    "action": "抢夺古玉", "state_delta": "古玉到手",
                }},
                {"id": "EVENT.2", "kind": "EVENT", "name": "中间转移", "payload": {
                    "active_actor": "CHAR.a", "provenance_refs": ["U.1"],
                    "causal_inputs": ["EVENT.1"], "causal_outputs": ["EVENT.3"],
                    "action": "遁入密道", "state_delta": "摆脱追兵",
                }},
                {"id": "EVENT.3", "kind": "EVENT", "name": "炼化古玉", "payload": {
                    "active_actor": "CHAR.a", "provenance_refs": ["U.1"], "time_index": 50,  # 严重时间倒流！
                    "causal_inputs": ["EVENT.2"], "causal_outputs": ["CHAR.a"],
                    "action": "炼化突破", "state_delta": "境界提升",
                }},
            ],
            "edges": [
                {"id": "E.p1", "type": "PARTICIPATES_IN", "source": "CHAR.a", "target": "EVENT.1", "payload": {"role": "initiator"}},
                {"id": "E.p2", "type": "PARTICIPATES_IN", "source": "CHAR.a", "target": "EVENT.2", "payload": {"role": "initiator"}},
                {"id": "E.p3", "type": "PARTICIPATES_IN", "source": "CHAR.a", "target": "EVENT.3", "payload": {"role": "initiator"}},
                {"id": "E.c1", "type": "CAUSES", "source": "EVENT.1", "target": "EVENT.2", "payload": {}},
                {"id": "E.c2", "type": "CAUSES", "source": "EVENT.2", "target": "EVENT.3", "payload": {}},
            ],
        }
        report = audit_packet(packet)
        self.assertFalse(report.ok)
        errors = {e["code"] for e in report.errors}
        self.assertIn("CAUSAL_ORDER_CONFLICT", errors)

    def test_webnovel_progression_roles_pass_capacity(self):
        payload = build_chapter_payload(["PRESSURE", "COUNTERMOVE", "CLIMAX", "PAYOFF"])
        chapter = {
            "id": "CHAPTER_PLAN.1",
            "kind": "CHAPTER_PLAN",
            "namespace": "PLAN",
            "payload": payload,
        }
        capacity = outline_agent.audit_chapter_capacity(chapter)
        self.assertEqual(capacity["final_capacity"], "FULL")
        self.assertEqual(capacity["mid_chapter_load"], "PASS")
    def test_unresolved_line_or_promise_fails_in_final_full_book(self):
        packet = build_demo_packet()
        packet["precision"] = {
            "production_stage": "FINAL_FULL_BOOK",
            "full_book_detailed_required": False,
        }
        packet["entities"].append({
            "id": "LINE.1", "kind": "LINE", "namespace": "PLAN",
            "payload": {"owner": "CHAR.a", "closure_condition": "cond", "status": "ACTIVE", "provenance_refs": ["USER.1"]},
        })
        packet["entities"].append({
            "id": "PROMISE.1", "kind": "PROMISE", "namespace": "PLAN",
            "payload": {
                "creation_event": "EVENT.1", "maturity_condition": "mat", "reveal_window": "win",
                "payoff_event": "EVENT.2", "status": "ACTIVE", "provenance_refs": ["USER.1"],
            },
        })
        report = audit_packet(packet)
        errors = {e["code"] for e in report.errors}
        self.assertIn("UNRESOLVED_FINALE_LINE", errors)
        self.assertIn("UNRESOLVED_FINALE_PROMISE", errors)

    def test_dead_actor_resurrection_fails_audit(self):
        packet = build_demo_packet()
        for e in packet["entities"]:
            if e["id"] == "CHAR.a":
                e["payload"]["death_chapter"] = 1
        ch_payload = build_chapter_payload(["ACTION", "COUNTERMOVE", "REPLAN", "HOOK"])
        ch_payload["chapter_no"] = 2
        ch_payload["active_actors"] = ["CHAR.a", "CHAR.b"]
        packet["entities"].append({
            "id": "CHAPTER_PLAN.2", "kind": "CHAPTER_PLAN", "namespace": "PLAN", "payload": ch_payload,
        })
        report = audit_packet(packet)
        errors = {e["code"] for e in report.errors}
        self.assertIn("DEAD_ACTOR_RESURRECTION", errors)

    def test_dynamic_fingerprint_chapter_capacity(self):
        payload = build_chapter_payload(["ACTION", "COUNTERMOVE", "REPLAN", "HOOK"])
        payload["target_prose_contract"]["chapter_mode"] = "ASSAULT"
        payload["dynamic_beats"][1]["active_actor"] = "CHAR.b"
        chapter = {
            "id": "CHAPTER_PLAN.1",
            "kind": "CHAPTER_PLAN",
            "namespace": "PLAN",
            "payload": payload,
        }
        capacity = outline_agent.audit_chapter_capacity(chapter, strict=True)
        self.assertEqual(capacity["final_capacity"], "FULL")

    def test_projector_preflight_allows_edges_between_new_batch_entities(self):
        class BatchEndpointProjector(GraphProjector):
            def __init__(self):
                super().__init__(shell="fake")

            def ensure_schema(self):
                return None

            def _run(self, cypher, params=None):
                if cypher == self.EDGE_PREFLIGHT:
                    return "edge_id\tsource_id\ttarget_id\n"
                return ""

        projector = BatchEndpointProjector()
        result = projector.sync("PROJECT.demo", [
            {
                "change_id": 1, "version": 1, "object_type": "ENTITY", "object_id": "CHAR.new",
                "action": "UPSERT", "before_json": None,
                "after_json": json.dumps({"entity_id": "CHAR.new", "kind": "CHARACTER", "name": "New", "namespace": "CANON", "status": "ACTIVE", "payload_json": "{}"}),
            },
            {
                "change_id": 2, "version": 1, "object_type": "ENTITY", "object_id": "EVENT.new",
                "action": "UPSERT", "before_json": None,
                "after_json": json.dumps({"entity_id": "EVENT.new", "kind": "EVENT", "name": "New Event", "namespace": "CANON", "status": "ACTIVE", "payload_json": "{}"}),
            },
            {
                "change_id": 3, "version": 1, "object_type": "EDGE", "object_id": "EDGE.new",
                "action": "UPSERT", "before_json": None,
                "after_json": json.dumps({
                    "edge_id": "EDGE.new", "edge_type": "CAUSES", "source_id": "CHAR.new",
                    "target_id": "EVENT.new", "namespace": "PLAN", "status": "ACTIVE",
                    "payload_json": "{}",
                }),
            },
        ])
        self.assertEqual(result.applied, 3)


if __name__ == "__main__":
    unittest.main()
