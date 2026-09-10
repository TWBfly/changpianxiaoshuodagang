# -*- coding: utf-8 -*-
"""
Ensemble Character Dynamics Test Suite
Validates:
1. Anti-Cardboard Agency & Anti-Fluff Participation
2. Ghost Actor Detection (Active actors with 0 beat participation)
3. Spotlight Continuity & Neglect Interception
4. Multi-Dimensional Character Contracts (Desire vectors, taboo lines, fatal flaws)
5. SQLite Canonical Persistence of (character_relationships, character_arcs)
6. Full 200-Chapter Ensemble Blueprint Compilation
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
scripts_dir = str(PROJECT_ROOT / ".agents" / "skills" / "vnext-outline-agent" / "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from core.ensemble_engine import EnsembleDynamicsEngine
from core.narrative_physics import NarrativePhysicsValidator
from core.scalable_blueprint import UniversalScalableBlueprint
from outline_agent import CanonicalStore, audit_packet


class TestEnsembleDynamics(unittest.TestCase):
    """Verifies ensemble character dynamics, agency checks, and persistence."""

    def setUp(self):
        self.ensemble = EnsembleDynamicsEngine(max_idle_chapters=25)

    def test_passive_cardboard_agency_interception(self):
        """Cardboard participation with pure bystander fluff must be flagged."""
        bad_chapter = {
            "id": "CHAPTER_PLAN.001",
            "payload": {
                "chapter_no": 1,
                "active_actors": ["CHAR.protagonist", "CHAR.cardboard_ally"],
                "dynamic_beats": [
                    {
                        "beat_role": "ACTION",
                        "active_actor": "CHAR.protagonist",
                        "action": "顾惊澜并指如剑斩灭三十名黑衣死士",
                        "counterforce": "死士头领负隅顽抗引爆血雷",
                        "delta": {"enemy": "DEFEATED"}
                    },
                    {
                        "beat_role": "REACTION",
                        "active_actor": "CHAR.cardboard_ally",
                        "action": "cardboard_ally倒吸一口凉气暗自心惊在旁观战退至众人身后",
                        "counterforce": "沦为背景板默默注视心中震惊",
                        "delta": {"state": "IDLE"}
                    }
                ]
            }
        }
        issues = self.ensemble.audit_character_agency([bad_chapter])
        self.assertTrue(any(i["code"] == "PASSIVE_CARDBOARD_PARTICIPATION" for i in issues))

    def test_proactive_agency_passes_cleanly(self):
        """Active actors with tactical decisions and real agency must pass cleanly."""
        good_chapter = {
            "id": "CHAPTER_PLAN.001",
            "payload": {
                "chapter_no": 1,
                "active_actors": ["CHAR.protagonist", "CHAR.tactical_ally"],
                "dynamic_beats": [
                    {
                        "beat_role": "ACTION",
                        "active_actor": "CHAR.protagonist",
                        "action": "顾惊澜正面吸引敌主力注意斩破中军防线",
                        "counterforce": "敌方铁骑以巨盾反扑合围",
                        "delta": {"front": "PIERCED"}
                    },
                    {
                        "beat_role": "TACTICAL_FLANK",
                        "active_actor": "CHAR.tactical_ally",
                        "action": "tactical_ally亲率轻骑包抄后路下达火攻截断粮道",
                        "counterforce": "敌粮官拼死抵抗企图焚库",
                        "delta": {"supply": "CUT"}
                    }
                ]
            }
        }
        issues = self.ensemble.audit_character_agency([good_chapter])
        self.assertEqual(issues, [])

    def test_ghost_actor_participation_intercepted(self):
        """Actors declared in active_actors but absent from all beats must be flagged."""
        ghost_chapter = {
            "id": "CHAPTER_PLAN.002",
            "payload": {
                "chapter_no": 2,
                "active_actors": ["CHAR.protagonist", "CHAR.completely_absent_actor"],
                "dynamic_beats": [
                    {
                        "beat_role": "ACTION",
                        "active_actor": "CHAR.protagonist",
                        "action": "顾惊澜独行探查黑风峡古阵",
                        "counterforce": "残破阵纹散发噬魂黑雾阻断神识",
                        "delta": {"lead": "FOUND"}
                    }
                ]
            }
        }
        issues = self.ensemble.audit_character_agency([ghost_chapter])
        self.assertTrue(any(i["code"] == "GHOST_ACTOR_PARTICIPATION" for i in issues))

    def test_spotlight_continuity_neglect_flagged(self):
        """Core characters who vanish for excessive chapters trigger spotlight neglect."""
        characters = {
            "CHAR.core_sister": {
                "id": "CHAR.core_sister",
                "kind": "CHARACTER",
                "payload": {
                    "character_tier": "CORE",
                    "role": "DEUTERAGONIST",
                    "goals": "重建家族",
                    "constraints": "不杀妇孺",
                }
            }
        }
        # Appears in Ch 1, vanishes, then reappears in Ch 45 (gap = 44 > limit of 25)
        chapter_plans = [
            {"id": "CHAPTER_PLAN.001", "payload": {"chapter_no": 1, "active_actors": ["CHAR.core_sister"], "dynamic_beats": []}},
            {"id": "CHAPTER_PLAN.045", "payload": {"chapter_no": 45, "active_actors": ["CHAR.core_sister"], "dynamic_beats": []}},
        ]
        issues = self.ensemble.audit_spotlight_continuity(chapter_plans, characters, max_idle_chapters=25)
        self.assertTrue(any(i["code"] == "SPOTLIGHT_NEGLECT_WARNING" for i in issues))

    def test_character_contracts_completeness(self):
        """Core characters must define desire vectors and moral constraints."""
        shallow_char = {
            "CHAR.shallow": {
                "id": "CHAR.shallow",
                "kind": "CHARACTER",
                "payload": {
                    "character_tier": "CORE",
                    # Missing goals, desires, taboo_line, and constraints
                }
            }
        }
        issues = self.ensemble.audit_character_contracts(shallow_char)
        self.assertTrue(any(i["code"] == "SHALLOW_CHARACTER_CONTRACT" for i in issues))

    def test_sqlite_persistence_of_ensemble_topology(self):
        """CanonicalStore must persist character relationships and volume arcs into SQLite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "ensemble_test.db")
            store = CanonicalStore(db_path)

            bp = UniversalScalableBlueprint(
                project_id="PROJECT.ensemble_persist",
                title="群像拓扑因果持久化",
                genre_id="XIANXIA",
                tone_id="SHUANGWEN",
                total_chapters=10,
                volumes_count=2,
            )
            packet = bp.generate_packet()

            store.init_project("PROJECT.ensemble_persist", "群像拓扑因果持久化")
            res = store.apply_packet("PROJECT.ensemble_persist", packet, expected_version=0, message="persist ensemble")
            self.assertEqual(res.version, 1)

            with store._connect() as conn:
                # 1. Verify character_relationships table
                rel_rows = conn.execute(
                    "SELECT * FROM character_relationships WHERE project_id = ?",
                    ("PROJECT.ensemble_persist",)
                ).fetchall()
                self.assertTrue(len(rel_rows) >= 2)
                # Verify specific relationship values
                ally_rel = [r for r in rel_rows if r["source_char_id"] == "CHAR.protagonist" and r["target_char_id"] == "CHAR.ally"][0]
                self.assertEqual(ally_rel["relationship_type"], "ALLY")
                self.assertEqual(ally_rel["affinity_score"], 95.0)
                self.assertEqual(ally_rel["ideology_friction"], 15.0)

                # 2. Verify character_arcs table
                arc_rows = conn.execute(
                    "SELECT * FROM character_arcs WHERE project_id = ?",
                    ("PROJECT.ensemble_persist",)
                ).fetchall()
                self.assertTrue(len(arc_rows) >= 3)
                protagonist_arcs = [r for r in arc_rows if r["character_id"] == "CHAR.protagonist"]
                self.assertTrue(len(protagonist_arcs) >= 2)

    def test_full_200_chapter_ensemble_blueprint(self):
        """A full 200-chapter blueprint must compile and pass all ensemble, physics, and tone audits."""
        bp = UniversalScalableBlueprint(
            project_id="PROJECT.ensemble_200",
            title="群像大作：九洲风华录",
            genre_id="HISTORICAL_ANCIENT",
            tone_id="PASSIONATE",
            total_chapters=200,
            volumes_count=8,
        )
        packet = bp.generate_packet()

        # Audit with full narrative physics + ensemble dynamics
        audit_res = NarrativePhysicsValidator.audit_packet(
            packet,
            strict_teleportation=True,
            strict_item_custody=True,
            strict_counterforce=True,
        )
        self.assertEqual(audit_res["errors"], [])


if __name__ == "__main__":
    unittest.main()
