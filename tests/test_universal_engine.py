# -*- coding: utf-8 -*-
"""
Universal Engine Test Suite (通用长篇小说大纲引擎综合因果与物理测试套件)
Covers:
1. Genre Drivers (Xianxia, Urban Horror, Infinite Flow, Honghuang)
2. 8 Dynamic Chapter Structure Fingerprints
3. Narrative Physics Validator (Spatiotemporal, Item Custody, Real Counterforce, Anti-Forgery)
4. Scalable Blueprint Generation & SQLite Canonical Persistence (200-ch Horror & 300-ch Honghuang)
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root and outline_agent scripts to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
scripts_dir = str(PROJECT_ROOT / ".agents" / "skills" / "vnext-outline-agent" / "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from genres import (
    get_genre_driver,
    list_registered_genres,
    XianxiaGenreDriver,
    HorrorGenreDriver,
    InfiniteFlowGenreDriver,
    HonghuangGenreDriver,
)
from core.dynamic_fingerprints import (
    validate_chapter_fingerprint,
    FINGERPRINT_SPECS,
)
from core.narrative_physics import (
    NarrativePhysicsValidator,
    BANNED_COUNTERFORCE_FLUFF,
)
from core.scalable_blueprint import UniversalScalableBlueprint
from outline_agent import CanonicalStore, audit_packet


class TestGenreDrivers(unittest.TestCase):
    """Verifies all 4 genre drivers and their worldview constraint mechanics."""

    def test_registered_genres(self):
        registered = list_registered_genres()
        self.assertIn("XIANXIA", registered)
        self.assertIn("HORROR", registered)
        self.assertIn("INFINITE_FLOW", registered)
        self.assertIn("HONGHUANG", registered)

    def test_xianxia_driver(self):
        driver = get_genre_driver("XIANXIA")
        self.assertIsInstance(driver, XianxiaGenreDriver)
        self.assertTrue(len(driver.power_levels) >= 8)
        self.assertTrue(len(driver.taboo_rules) >= 3)
        
        # Test modern word immersion violation
        banned = driver.check_immersion_lexicon("他在大殿上演示了PPT报表和现代分权")
        self.assertTrue(any("PPT" in msg for msg in banned))
        self.assertTrue(any("现代分权" in msg for msg in banned))

        # Test breakthrough without cost violation
        payload_fluff = {
            "chapter_no": 5,
            "dynamic_beats": [
                {"role": "ACTION", "action": "主角连破三阶突破金丹", "counterforce": "敌人震惊退缩"}
            ]
        }
        violations = driver.validate_chapter_mechanics(payload_fluff)
        self.assertTrue(any("Cultivation breakthrough lacks required tribulation/cost" in v for v in violations))

    def test_horror_driver(self):
        driver = get_genre_driver("HORROR")
        self.assertIsInstance(driver, HorrorGenreDriver)
        self.assertIn("理智值 (Sanity Points)", driver.currencies)
        
        # Test violation: ghost killed with mortal weapon
        payload = {
            "chapter_no": 12,
            "dynamic_beats": [
                {"role": "ACTION", "action": "主角用凡铁菜刀正面砍死红衣厉鬼", "counterforce": "厉鬼惨叫灰飞烟灭"}
            ]
        }
        violations = driver.validate_chapter_mechanics(payload)
        self.assertTrue(any("Mortal physical weapons cannot permanently kill an entity" in v for v in violations))

    def test_infinite_flow_driver(self):
        driver = get_genre_driver("INFINITE_FLOW")
        self.assertIsInstance(driver, InfiniteFlowGenreDriver)
        self.assertTrue(any("Reward Points" in c for c in driver.currencies))
        
        # Test modern words in historical realm
        payload = {
            "chapter_no": 3,
            "realm_mode": "HISTORICAL",
            "dynamic_beats": [
                {"role": "ACTION", "action": "在三国战场主角掏出智能手机打开维基百科", "counterforce": "曹操大惊"}
            ]
        }
        violations = driver.validate_chapter_mechanics(payload)
        self.assertTrue(any("Anachronistic element" in v for v in violations))

    def test_honghuang_driver(self):
        driver = get_genre_driver("HONGHUANG")
        self.assertIsInstance(driver, HonghuangGenreDriver)
        self.assertTrue(any("混元大罗金仙" in lvl for lvl in driver.power_levels))
        
        # Test saint dying without karma tribulation
        payload = {
            "chapter_no": 50,
            "dynamic_beats": [
                {"role": "ACTION", "action": "金仙主角一拳斩杀天道圣人", "counterforce": "圣人陨落天地同悲"}
            ]
        }
        violations = driver.validate_chapter_mechanics(payload)
        self.assertTrue(any("Saint killed or subdued without supreme Karma/Tribulation" in v for v in violations))


class TestDynamicFingerprints(unittest.TestCase):
    """Verifies all 8 dynamic chapter structure fingerprints."""

    def test_all_eight_fingerprints_recognized(self):
        modes = ["ASSAULT", "INVESTIGATION", "CRISIS", "ENSEMBLE", "PURSUIT", "TRIAL", "GOVERNANCE", "LIFESTYLE"]
        for m in modes:
            self.assertIn(m, FINGERPRINT_SPECS)
            spec = FINGERPRINT_SPECS[m]
            self.assertTrue(spec.min_beats >= 3)
            self.assertTrue(spec.max_beats >= spec.min_beats)
            self.assertTrue(len(spec.required_roles) >= 3)

    def test_assault_fingerprint_valid_and_invalid(self):
        valid_payload = {
            "chapter_mode": "ASSAULT",
            "dynamic_beats": [
                {"role": "ACTION", "action": "破关"},
                {"role": "COUNTERMOVE", "action": "反制"},
                {"role": "BREAKTHROUGH", "action": "突破"},
                {"role": "HOOK", "action": "钩子"},
            ],
            "scene_payloads": [{"scene_id": "S1"}],
        }
        errs = validate_chapter_fingerprint(valid_payload)
        self.assertEqual(errs, [])

        # Missing BREAKTHROUGH
        invalid_payload = {
            "chapter_mode": "ASSAULT",
            "dynamic_beats": [
                {"role": "ACTION", "action": "破关"},
                {"role": "COUNTERMOVE", "action": "反制"},
                {"role": "HOOK", "action": "钩子"},
            ],
            "scene_payloads": [{"scene_id": "S1"}],
        }
        errs = validate_chapter_fingerprint(invalid_payload)
        self.assertTrue(len(errs) > 0)
        self.assertTrue(any("missing required beat role: 'BREAKTHROUGH'" in e for e in errs))


class TestNarrativePhysics(unittest.TestCase):
    """Verifies spatiotemporal, item chain of custody, and counterforce integrity."""

    def setUp(self):
        self.validator = NarrativePhysicsValidator()

    def test_spatiotemporal_time_reversion(self):
        plans = [
            {"id": "CP1", "payload": {"chapter_no": 1, "spacetime": {"story_day": 5.0, "location_id": "LOC.A"}}},
            {"id": "CP2", "payload": {"chapter_no": 2, "spacetime": {"story_day": 3.0, "location_id": "LOC.A"}}},
        ]
        issues = self.validator.audit_spatiotemporal_continuity(plans)
        self.assertTrue(any(iss["code"] in {"TEMPORAL_REGRESSION", "TIME_REVERSION"} for iss in issues))

    def test_spatiotemporal_teleportation(self):
        plans = [
            {"id": "CP1", "payload": {"chapter_no": 1, "spacetime": {"story_day": 1.0, "location_id": "LOC.A"}}},
            {"id": "CP2", "payload": {
                "chapter_no": 2,
                "spacetime": {
                    "story_day": 1.0,
                    "location_id": "LOC.B",
                    "travel_mode": "WALK",
                    "distance_traveled": 5000.0,
                }
            }},
        ]
        issues = self.validator.audit_spatiotemporal_continuity(plans)
        self.assertTrue(any(iss["code"] in {"SPATIOTEMPORAL_TELEPORTATION_VIOLATION", "IMPOSSIBLE_TELEPORTATION"} for iss in issues))

    def test_item_custody_premature_use(self):
        props = {
            "PROP.god_sword": {
                "id": "PROP.god_sword",
                "payload": {"status": "ACTIVE", "owner": "CHAR.protagonist", "introduced_in_chapter": 10},
            }
        }
        plans = [
            {"id": "CP1", "payload": {"chapter_no": 2, "items_used": ["PROP.god_sword"], "dynamic_beats": []}},
        ]
        issues = self.validator.audit_item_chain_of_custody(plans, props)
        self.assertTrue(any(iss["code"] == "CHAIN_OF_CUSTODY_VIOLATION" for iss in issues))
        self.assertTrue(any("before introduced at Ch 10" in iss["message"] for iss in issues))

    def test_item_custody_destroyed_item_use(self):
        props = {
            "PROP.elixir": {
                "id": "PROP.elixir",
                "payload": {"status": "ACTIVE", "owner": "CHAR.protagonist", "introduced_in_chapter": 1},
            }
        }
        plans = [
            {
                "id": "CP1",
                "payload": {
                    "chapter_no": 1,
                    "items_used": ["PROP.elixir"],
                    "item_events": [{"item_id": "PROP.elixir", "action": "CONSUME"}],
                    "dynamic_beats": [],
                }
            },
            {
                "id": "CP2",
                "payload": {
                    "chapter_no": 2,
                    "items_used": ["PROP.elixir"],
                    "dynamic_beats": [],
                }
            },
        ]
        issues = self.validator.audit_item_chain_of_custody(plans, props)
        self.assertTrue(any(iss["code"] == "CHAIN_OF_CUSTODY_VIOLATION" for iss in issues))
        self.assertTrue(any("after being marked as DESTROYED" in iss["message"] for iss in issues))

    def test_counterforce_fluff_rejection(self):
        characters = {
            "CHAR.protagonist": {"name": "顾惊澜", "payload": {"aliases": ["少帅"]}}
        }
        plans = [
            {
                "id": "CP1",
                "payload": {
                    "chapter_no": 1,
                    "dynamic_beats": [
                        {
                            "beat_id": "B1",
                            "active_actor": "CHAR.protagonist",
                            "action": "顾惊澜挥剑破阵杀出重围",
                            "counterforce": "展现横推一切之无敌神威",
                        }
                    ]
                }
            }
        ]
        # In strict mode, fluff must be rejected as an error
        issues = self.validator.audit_counterforce_and_actor_authenticity(
            plans, characters=characters, strict_counterforce=True
        )
        self.assertTrue(any(iss["code"] == "FLUFF_COUNTERFORCE_REJECTED" for iss in issues))

    def test_anti_actor_forgery(self):
        characters = {
            "CHAR.villain": {"name": "慕容渊", "payload": {"aliases": []}}
        }
        plans = [
            {
                "id": "CP1",
                "payload": {
                    "chapter_no": 1,
                    "dynamic_beats": [
                        {
                            "beat_id": "B1",
                            "active_actor": "CHAR.villain",
                            "action": "张三李四在茶馆喝茶聊天",
                            "counterforce": "茶水已凉",
                        }
                    ]
                }
            }
        ]
        issues = self.validator.audit_counterforce_and_actor_authenticity(
            plans, characters=characters, strict_counterforce=True
        )
        self.assertTrue(any(iss["code"] == "ACTOR_FORGERY_LABEL_MISMATCH" for iss in issues))


class TestScalableBlueprintEngine(unittest.TestCase):
    """Verifies generation of 200-chapter Horror and 300-chapter Honghuang novel blueprints."""

    def test_200_chapter_urban_horror_compilation(self):
        bp = UniversalScalableBlueprint(
            project_id="PROJECT.horror_200",
            title="诡异规则怪谈：我在迷雾中守夜",
            genre_id="HORROR",
            total_chapters=200,
            volumes_count=8,
            synopsis="一部200章现代规则怪谈与民俗禁忌调查长篇小说。",
        )
        packet = bp.build_full_packet()

        self.assertEqual(packet["target_chapters"], 200)
        self.assertEqual(packet["genre"], "HORROR")

        # Verify volume entities
        volumes = [e for e in packet["entities"] if e["kind"] == "VOLUME"]
        self.assertEqual(len(volumes), 8)

        # Verify chapter plans
        chapter_plans = [e for e in packet["entities"] if e["kind"] == "CHAPTER_PLAN"]
        self.assertEqual(len(chapter_plans), 200)

        # Verify 8 dynamic fingerprints are distributed across chapters
        modes_observed = {cp["payload"]["chapter_mode"] for cp in chapter_plans}
        self.assertTrue(len(modes_observed) >= 7)

        # Run NarrativePhysicsValidator on the entire 200-chapter packet
        physics_report = NarrativePhysicsValidator.audit_packet(
            packet,
            strict_teleportation=True,
            strict_item_custody=True,
            strict_counterforce=True,
        )
        self.assertEqual(physics_report["errors"], [])

    def test_300_chapter_honghuang_compilation(self):
        bp = UniversalScalableBlueprint(
            project_id="PROJECT.honghuang_300",
            title="洪荒圣劫：人道截天录",
            genre_id="HONGHUANG",
            total_chapters=300,
            volumes_count=10,
            synopsis="一部300章洪荒封神与诸圣因果杀劫史诗巨制。",
        )
        packet = bp.build_full_packet()

        self.assertEqual(packet["target_chapters"], 300)
        self.assertEqual(packet["genre"], "HONGHUANG")

        volumes = [e for e in packet["entities"] if e["kind"] == "VOLUME"]
        self.assertEqual(len(volumes), 10)

        chapter_plans = [e for e in packet["entities"] if e["kind"] == "CHAPTER_PLAN"]
        self.assertEqual(len(chapter_plans), 300)

        # Full audit
        audit_res = NarrativePhysicsValidator.audit_packet(
            packet,
            strict_teleportation=True,
            strict_item_custody=True,
            strict_counterforce=True,
        )
        self.assertEqual(audit_res["errors"], [])

    def test_sqlite_canonical_persistence(self):
        """Verifies database migrations and table insertion in SQLite CanonicalStore."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "canon.db")
            store = CanonicalStore(db_path)

            bp = UniversalScalableBlueprint(
                project_id="PROJECT.persist_test",
                title="因果持久化验证",
                genre_id="XIANXIA",
                total_chapters=10,
                volumes_count=2,
            )
            packet = bp.build_full_packet()

            # Initialize project and apply packet to CanonicalStore
            store.init_project("PROJECT.persist_test", "因果持久化验证")
            res = store.apply_packet("PROJECT.persist_test", packet, expected_version=0, message="test apply")
            self.assertEqual(res.version, 1)

            # Query the newly migrated tables
            with store._connect() as conn:
                # 1. Spacetime table
                st_rows = conn.execute("SELECT * FROM chapter_spacetime").fetchall()
                self.assertEqual(len(st_rows), 10)
                # Verify day monotonicity
                days = [r["story_day"] for r in st_rows]
                self.assertEqual(days, sorted(days))

                # 2. Project table migration columns
                proj_row = conn.execute("SELECT genre, target_chapters FROM projects WHERE project_id = ?", ("PROJECT.persist_test",)).fetchone()
                self.assertIsNotNone(proj_row)
                self.assertEqual(proj_row["genre"], "XIANXIA")
                self.assertEqual(proj_row["target_chapters"], 10)


if __name__ == "__main__":
    unittest.main()
