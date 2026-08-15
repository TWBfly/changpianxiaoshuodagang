import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

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


class CanonicalStoreTests(unittest.TestCase):
    def test_init_creates_version_zero_and_empty_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CanonicalStore(Path(tmp) / "outline.db")
            self.assertEqual(store.init_project("PROJECT.demo", "Demo"), 0)
            self.assertEqual(store.get_version("PROJECT.demo"), 0)

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
            self.assertEqual(sum(line.startswith("- `CHAR.") for line in text.splitlines()), 2)

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


if __name__ == "__main__":
    unittest.main()
