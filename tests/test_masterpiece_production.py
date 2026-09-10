# -*- coding: utf-8 -*-
"""
Masterpiece Production Benchmark Suite (工业级多流派长篇小说全息大纲生产基准测试)

Verifies that UniversalScalableBlueprint produces production-ready, publication-grade
novel blueprints (200 chapters each) across multiple distinct genres and tones:
1. URBAN_REALISTIC + SHUANGWEN (都市现实商战 / 爽文升级)
2. CTHULHU_WESTERN + SUSPENSE_SERIOUS (克苏鲁奇幻调查 / 悬疑严肃)
3. SCI_FI_CYBER + PASSIONATE (赛博朋克科幻 / 热血激昂)
4. HISTORICAL_ANCIENT + TRAGIC_EPIC (架空历史权谋 / 悲壮史诗)

Quality Gates Enforced:
- No placeholder strings ("主角", "宿敌", "核心盟友", "反派")
- 6 genuine genre-adapted characters with full 9-field contracts
- 6 distributed storylines (LINE) with distinct owners
- 200 chapters with PRODUCTION_READY schema (4000-6000 words, 4 STAGEABLE_CORE beats, 2 clusters, 2 scenes)
- Multi-agent rotating active actors across 8 dynamic chapter fingerprints
- Zero CORE_CHARACTER_ZERO_ACTION errors
- Zero SPOTLIGHT_HEAD_NEGLECT_WARNING or SPOTLIGHT_TAIL_NEGLECT_WARNING
- Zero STORYLINE_OWNER_CONCENTRATION warnings
- Zero FORGED_ACTOR_SUSPECT warnings
- Full audit_packet passes with 0 errors and 0 warnings (strict mode)
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Add project root and outline_agent scripts to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
scripts_dir = str(PROJECT_ROOT / ".agents" / "skills" / "vnext-outline-agent" / "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from core.ensemble_engine import (
    audit_character_contracts,
    audit_ensemble_spotlight,
    audit_storyline_ownership,
)
from core.narrative_physics import NarrativePhysicsValidator
from core.scalable_blueprint import UniversalScalableBlueprint
from outline_agent import audit_packet


class TestMasterpieceProduction(unittest.TestCase):
    """Rigorous end-to-end verification for N different novel masterpieces."""

    def _verify_masterpiece_packet(
        self,
        packet: dict,
        expected_genre: str,
        expected_chapters: int = 200,
        expected_volumes: int = 8,
    ):
        """Universal quality gate assertion function for any novel packet."""
        # 1. Basic packet metadata
        self.assertEqual(packet["target_chapters"], expected_chapters)
        self.assertEqual(packet["genre"], expected_genre)
        self.assertTrue(packet["strict_mode"])

        # 2. Extract entities
        entities = packet["entities"]
        characters = [e for e in entities if e["kind"] == "CHARACTER"]
        lines = [e for e in entities if e["kind"] == "LINE"]
        volumes = [e for e in entities if e["kind"] == "VOLUME"]
        chapter_plans = [e for e in entities if e["kind"] == "CHAPTER_PLAN"]

        self.assertEqual(len(characters), 6, "Must provide a 6-character ensemble")
        self.assertEqual(len(lines), 6, "Must provide 6 distinct distributed storylines")
        self.assertEqual(len(volumes), expected_volumes, f"Must have {expected_volumes} volumes")
        self.assertEqual(len(chapter_plans), expected_chapters, f"Must have {expected_chapters} chapters")

        # 3. Anti-placeholder check: Character names must be genuine genre names
        placeholder_strings = {"主角", "宿敌", "核心盟友", "反派", "导师", "配角", "龙套"}
        for char in characters:
            c_name = char["name"]
            for ph in placeholder_strings:
                self.assertNotIn(
                    ph,
                    c_name,
                    f"Character name '{c_name}' contains illegal placeholder '{ph}'",
                )

        # 4. Character contracts audit
        char_dict = {c["id"]: c for c in characters}
        contract_issues = audit_character_contracts(char_dict)
        self.assertEqual(
            contract_issues,
            [],
            f"Character contract audit failed: {contract_issues}",
        )

        # 5. Storyline ownership audit: distributed ownership across characters
        line_issues = audit_storyline_ownership(lines, char_dict)
        self.assertEqual(
            line_issues,
            [],
            f"Storyline ownership audit failed: {line_issues}",
        )

        # 6. Chapter Capacity & Schema audit: all chapters must be PRODUCTION_READY
        fingerprints_used = set()
        active_actors_seen = set()
        for cp in chapter_plans:
            payload = cp["payload"]
            c_no = payload["chapter_no"]

            # Capacity
            contract = payload.get("target_prose_contract", {})
            self.assertGreaterEqual(contract.get("target_min", 0), 4000)
            self.assertLessEqual(contract.get("target_max", 0), 6000)

            # Beats
            beats = payload["dynamic_beats"]
            self.assertGreaterEqual(len(beats), 4, f"Ch {c_no} must have at least 4 beats")
            for b in beats:
                self.assertEqual(
                    b.get("stageability"),
                    "STAGEABLE_CORE",
                    f"Ch {c_no} beat {b.get('beat_id')} must be STAGEABLE_CORE",
                )
                self.assertIn(
                    b.get("active_actor"),
                    char_dict,
                    f"Ch {c_no} active_actor '{b.get('active_actor')}' must be in character cast",
                )
                active_actors_seen.add(b.get("active_actor"))

            # Clusters and scenes
            self.assertEqual(len(payload.get("payload_clusters", [])), 2)
            self.assertEqual(len(payload.get("scene_payloads", [])), 2)

            fingerprints_used.add(payload.get("chapter_mode"))

        # Must use all 8 dynamic chapter fingerprints across 200 chapters
        self.assertEqual(
            len(fingerprints_used),
            8,
            f"Expected all 8 chapter fingerprints to be utilized, found: {fingerprints_used}",
        )

        # All characters must have acted
        self.assertEqual(
            active_actors_seen,
            set(char_dict.keys()),
            "Every character in the 6-person ensemble must actively act in beats",
        )

        # 7. Ensemble spotlight audit: zero zero-action, zero neglect warnings
        spotlight_issues = audit_ensemble_spotlight(
            char_dict,
            chapter_plans,
            total_chapters=expected_chapters,
        )
        spotlight_errors = [iss for iss in spotlight_issues if not iss.get("is_warning", True)]
        spotlight_warnings = [iss for iss in spotlight_issues if iss.get("is_warning", True)]
        self.assertEqual(spotlight_errors, [], f"Spotlight errors found: {spotlight_errors}")
        self.assertEqual(spotlight_warnings, [], f"Spotlight warnings found: {spotlight_warnings}")

        # 8. Full end-to-end audit_packet with strict counterforce
        audit_res = audit_packet(packet, strict_counterforce=True)
        self.assertEqual(
            audit_res["errors"],
            [],
            f"Full audit_packet returned errors: {audit_res['errors']}",
        )
        self.assertEqual(
            audit_res["warnings"],
            [],
            f"Full audit_packet returned warnings: {audit_res['warnings']}",
        )

    def test_urban_realistic_200_chapter_production(self):
        """Production benchmark: Urban Realistic Commercial Thriller (200 Chapters)."""
        bp = UniversalScalableBlueprint(
            project_id="PROJECT.urban_real_200",
            title="商海狂澜：资本猎手的破晓对决",
            genre_id="URBAN_REALISTIC",
            total_chapters=200,
            volumes_count=8,
            synopsis="一部200章现代都市商战、并购反垄断与多方利益博弈的鸿篇巨制。",
            tone_id="SHUANGWEN",
        )
        packet = bp.build_full_packet()
        self._verify_masterpiece_packet(packet, expected_genre="URBAN_REALISTIC")

    def test_cthulhu_western_200_chapter_production(self):
        """Production benchmark: Cthulhu Western Investigation (200 Chapters)."""
        bp = UniversalScalableBlueprint(
            project_id="PROJECT.cthulhu_200",
            title="旧日残响：密斯卡托尼克的守夜人",
            genre_id="CTHULHU_WESTERN",
            total_chapters=200,
            volumes_count=8,
            synopsis="一部200章西方克苏鲁禁忌探秘、理智抗争与古神博弈的长篇悬疑史诗。",
            tone_id="SUSPENSE_SERIOUS",
        )
        packet = bp.build_full_packet()
        self._verify_masterpiece_packet(packet, expected_genre="CTHULHU_WESTERN")

    def test_scifi_cyber_200_chapter_production(self):
        """Production benchmark: Sci-Fi Cyberpunk Action (200 Chapters)."""
        bp = UniversalScalableBlueprint(
            project_id="PROJECT.cyber_200",
            title="霓虹死局：义体黑客的黎明狂飙",
            genre_id="SCI_FI_CYBER",
            total_chapters=200,
            volumes_count=8,
            synopsis="一部200章近未来赛博朋克义体革命、脑机垄断破除与热血突围长篇巨制。",
            tone_id="PASSIONATE",
        )
        packet = bp.build_full_packet()
        self._verify_masterpiece_packet(packet, expected_genre="SCI_FI_CYBER")

    def test_historical_ancient_200_chapter_production(self):
        """Production benchmark: Historical Ancient Political Epic (200 Chapters)."""
        bp = UniversalScalableBlueprint(
            project_id="PROJECT.historical_200",
            title="山河铁血：北境巡抚的挽歌纪事",
            genre_id="HISTORICAL_ANCIENT",
            total_chapters=200,
            volumes_count=8,
            synopsis="一部200章架空历史王朝权谋、边陲铁骑争锋与士族倾轧的悲壮长篇巨作。",
            tone_id="TRAGIC_EPIC",
        )
        packet = bp.build_full_packet()
        self._verify_masterpiece_packet(packet, expected_genre="HISTORICAL_ANCIENT")


if __name__ == "__main__":
    unittest.main()
