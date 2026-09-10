# -*- coding: utf-8 -*-
"""
Genre and Tone Matrix Test Suite
Validates:
1. All 13 Web Novel Genres + Dynamic Custom Genre Creation
2. All 6 Emotional Tones + Dynamic Custom Tone Creation
3. Tone Auditing (Payoffs, Forbidden Tropes, Pacing Constraints)
4. Full Scalable Blueprints (200-ch) across Genre x Tone Cross Combinations
5. SQLite Persistence of (genre, tone) in projects table
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

import genres
import tones
from core.narrative_physics import NarrativePhysicsValidator
from core.scalable_blueprint import UniversalScalableBlueprint
from outline_agent import CanonicalStore, audit_packet


class TestGenreAndToneMatrix(unittest.TestCase):
    """Verifies all web novel genres, emotional tones, and their combinatorial compilation."""

    def test_all_thirteen_genres_registered(self):
        expected_genres = [
            "XIANXIA", "HORROR", "INFINITE_FLOW", "HONGHUANG",
            "URBAN_REALISTIC", "URBAN_SUPERNATURAL", "HISTORICAL_ANCIENT",
            "SUSPENSE_DETECTIVE", "BRAIN_HOLE", "REPUBLIC_ERA",
            "CTHULHU_WESTERN", "SCI_FI_CYBER", "GAME_SYSTEM"
        ]
        registered = genres.list_registered_genres()
        for g in expected_genres:
            self.assertIn(g, registered, f"Genre {g} must be registered.")
            driver = genres.get_genre_driver(g)
            self.assertTrue(len(driver.power_levels) >= 4)
            self.assertTrue(len(driver.currencies) >= 3)
            self.assertTrue(len(driver.taboo_rules) >= 2)

    def test_genre_aliases(self):
        alias_map = {
            "dushi": "URBAN_REALISTIC",
            "dushi_xiuxian": "URBAN_SUPERNATURAL",
            "dushi_yineng": "URBAN_SUPERNATURAL",
            "jiakong": "HISTORICAL_ANCIENT",
            "xuanyi": "SUSPENSE_DETECTIVE",
            "naodong": "BRAIN_HOLE",
            "minguo": "REPUBLIC_ERA",
            "cthulhu": "CTHULHU_WESTERN",
            "kesulu": "CTHULHU_WESTERN",
            "kehuan": "SCI_FI_CYBER",
            "scifi": "SCI_FI_CYBER",
            "youxi": "GAME_SYSTEM",
            "wuxian": "INFINITE_FLOW",
            "honghuang": "HONGHUANG",
        }
        for alias, expected in alias_map.items():
            driver = genres.get_genre_driver(alias)
            self.assertEqual(driver.genre_id, expected)

    def test_dynamic_custom_genre_creation(self):
        custom = genres.create_custom_genre(
            genre_id="APOCALYPTIC_WASTELAND",
            genre_name="末世废土生存 (Apocalyptic Wasteland)",
            description="核冬天与基因突变生物的世界",
            power_levels=["避难所难民", "辐射猎人", "基因改造战将", "废土主宰"],
            currencies=["纯净水", "午餐肉罐头", "防辐射血清", "无缝钢管弹药"],
            taboo_rules=["重度辐射无防护三分钟致死", "热量赤字不可逆消耗"],
            banned_words=["金丹", "元婴", "天劫"]
        )
        self.assertIn("APOCALYPTIC_WASTELAND", genres.list_registered_genres())
        retrieved = genres.get_genre_driver("APOCALYPTIC_WASTELAND")
        self.assertEqual(retrieved.genre_name, "末世废土生存 (Apocalyptic Wasteland)")
        # Test banned words
        violations = retrieved.validate_chapter_mechanics({"chapter_no": 1, "text": "主角凝聚了元婴"})
        self.assertTrue(len(violations) > 0)

    def test_all_six_tones_registered(self):
        expected_tones = [
            "SHUANGWEN", "HUMOR", "SUSPENSE_SERIOUS",
            "ANGUISH", "TRAGIC_EPIC", "PASSIONATE"
        ]
        registered = tones.list_registered_tones()
        for t in expected_tones:
            self.assertIn(t, registered, f"Tone {t} must be registered.")
            driver = tones.get_tone_driver(t)
            self.assertTrue(len(driver.required_emotional_payoffs) >= 4)
            self.assertTrue(len(driver.forbidden_tone_tropes) >= 3)

    def test_shuangwen_tone_prolonged_oppression_check(self):
        shuang_driver = tones.get_tone_driver("SHUANGWEN")
        # 3 beats of pure passive humiliation without counterplay -> should flag
        bad_payload = {
            "chapter_no": 5,
            "dynamic_beats": [
                {"beat_role": "ACTION", "action": "反派扇耳光", "counterforce": "主角遭受践踏凌辱无法动弹"},
                {"beat_role": "ACTION", "action": "反派夺宝", "counterforce": "主角重创垂死绝望无力"},
                {"beat_role": "ACTION", "action": "反派踩头", "counterforce": "主角继续绝望无力受辱"},
            ]
        }
        violations = shuang_driver.validate_chapter_tone(bad_payload)
        self.assertTrue(any("Excessive prolonged passive oppression" in v for v in violations))

    def test_forbidden_tone_tropes_intercepted(self):
        # 1. Humor tone with heavy gloomy trope
        humor_driver = tones.get_tone_driver("HUMOR")
        humor_bad = {"chapter_no": 1, "text": "本章气氛苦大仇深全篇压抑毫无笑料"}
        self.assertTrue(len(humor_driver.validate_chapter_tone(humor_bad)) > 0)

        # 2. Suspense tone with deus ex machina trope
        suspense_driver = tones.get_tone_driver("SUSPENSE_SERIOUS")
        suspense_bad = {"chapter_no": 1, "text": "主角使用了机械降神瞬间破案"}
        self.assertTrue(len(suspense_driver.validate_chapter_tone(suspense_bad)) > 0)

        # 3. Anguish tone with cheap resurrection trope
        anguish_driver = tones.get_tone_driver("ANGUISH")
        anguish_bad = {"chapter_no": 1, "text": "主角死而复生消解全部悲剧重量"}
        self.assertTrue(len(anguish_driver.validate_chapter_tone(anguish_bad)) > 0)

        # 4. Tragic Epic tone with clowning trope
        tragic_driver = tones.get_tone_driver("TRAGIC_EPIC")
        tragic_bad = {"chapter_no": 1, "text": "城破之时主角嬉皮笑脸消解崇高感"}
        self.assertTrue(len(tragic_driver.validate_chapter_tone(tragic_bad)) > 0)

        # 5. Passionate tone with betrayal trope
        passionate_driver = tones.get_tone_driver("PASSIONATE")
        passionate_bad = {"chapter_no": 1, "text": "决战时刻主角利己精算背弃生死挚友"}
        self.assertTrue(len(passionate_driver.validate_chapter_tone(passionate_bad)) > 0)

    def test_dynamic_custom_tone_creation(self):
        custom = tones.create_custom_tone(
            tone_id="DARK_CYNICAL",
            tone_name="黑道冷血与犬儒反英雄 (Dark Cynical)",
            description="利益至上、黑暗森林、绝对理智冷酷",
            forbidden_tone_tropes=["突然圣母心发作拯救世界"]
        )
        self.assertIn("DARK_CYNICAL", tones.list_registered_tones())
        retrieved = tones.get_tone_driver("DARK_CYNICAL")
        violations = retrieved.validate_chapter_tone({"chapter_no": 1, "text": "主角突然圣母心发作拯救世界"})
        self.assertTrue(len(violations) > 0)

    def test_cross_genre_tone_blueprint_compilation(self):
        """
        Tests generation and causal/physics/tone auditing of 200-chapter blueprints
        across distinct Genre x Tone cross-combinations.
        """
        test_matrix = [
            ("PROJECT.dushi_humor_200", "我把异能玩成了沙雕", "URBAN_SUPERNATURAL", "HUMOR", 200),
            ("PROJECT.history_tragic_200", "大明孤臣挽天倾", "HISTORICAL_ANCIENT", "TRAGIC_EPIC", 200),
            ("PROJECT.cthulhu_suspense_200", "密斯卡托尼克法医探案录", "CTHULHU_WESTERN", "SUSPENSE_SERIOUS", 200),
            ("PROJECT.scifi_passionate_200", "星火燎原：人类战旗不倒", "SCI_FI_CYBER", "PASSIONATE", 200),
            ("PROJECT.brainhole_shuang_200", "概念神：反向打钱横推一切", "BRAIN_HOLE", "SHUANGWEN", 200),
            ("PROJECT.republic_suspense_200", "津门暗谍：潜伏者没有名字", "REPUBLIC_ERA", "SUSPENSE_SERIOUS", 200),
            ("PROJECT.game_shuang_200", "第四天灾之基建狂魔", "GAME_SYSTEM", "SHUANGWEN", 200),
        ]

        for p_id, title, genre_id, tone_id, ch_count in test_matrix:
            with self.subTest(genre=genre_id, tone=tone_id):
                bp = UniversalScalableBlueprint(
                    project_id=p_id,
                    title=title,
                    genre_id=genre_id,
                    tone_id=tone_id,
                    total_chapters=ch_count,
                    volumes_count=8,
                )
                packet = bp.generate_packet()

                self.assertEqual(packet["genre"], genres.get_genre_driver(genre_id).genre_id)
                self.assertEqual(packet["tone"], tones.get_tone_driver(tone_id).tone_id)
                self.assertEqual(packet["target_chapters"], ch_count)

                # Validate full narrative physics & tone
                audit_res = NarrativePhysicsValidator.audit_packet(
                    packet,
                    strict_teleportation=True,
                    strict_item_custody=True,
                    strict_counterforce=True,
                )
                self.assertEqual(audit_res["errors"], [], f"Errors in {title}: {audit_res['errors']}")

    def test_sqlite_persistence_with_genre_and_tone(self):
        """Verifies that CanonicalStore persists both genre and tone into SQLite projects table."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "novel_matrix.db")
            store = CanonicalStore(db_path)

            bp = UniversalScalableBlueprint(
                project_id="PROJECT.matrix_persist",
                title="全息矩阵持久化验证",
                genre_id="CTHULHU_WESTERN",
                tone_id="SUSPENSE_SERIOUS",
                total_chapters=20,
                volumes_count=2,
            )
            packet = bp.generate_packet()

            store.init_project("PROJECT.matrix_persist", "全息矩阵持久化验证")
            res = store.apply_packet("PROJECT.matrix_persist", packet, expected_version=0, message="persist matrix")
            self.assertEqual(res.version, 1)

            with store._connect() as conn:
                row = conn.execute(
                    "SELECT genre, tone, target_chapters FROM projects WHERE project_id = ?",
                    ("PROJECT.matrix_persist",)
                ).fetchone()
                self.assertIsNotNone(row)
                self.assertEqual(row["genre"], "CTHULHU_WESTERN")
                self.assertEqual(row["tone"], "SUSPENSE_SERIOUS")
                self.assertEqual(row["target_chapters"], 20)


if __name__ == "__main__":
    unittest.main()
