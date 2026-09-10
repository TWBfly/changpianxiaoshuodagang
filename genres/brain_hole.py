# -*- coding: utf-8 -*-
"""
Brain Hole & High-Concept Genre Driver
Covers innovative concepts, meme-rule subversion, item tag extraction,
reality manipulation systems, and meta-narrative concept logic.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class BrainHoleGenreDriver(BaseGenreDriver):
    genre_id = "BRAIN_HOLE"
    genre_name = "脑洞创意与概念神流 (Brain Hole & High-Concept)"
    description = "以极其清奇的底层核心设定、概念词条提取、反常规规则颠覆与推演闭环为核心的世界观。"

    power_levels = [
        "概念初见觉醒",
        "词条掠夺/概念拼接者",
        "认知篡改/规则重塑者",
        "现实扭曲/维度定义者",
        "因果奇点/叙事层主宰",
    ]

    currencies = [
        "认知冲击点数 (Cognitive Shock Points)",
        "概念因果币 (Conceptual Causality Coins)",
        "扭曲现实代币 (Reality Distortion Chips)",
        "万物词条碎片 (Item Affix Shards)",
    ]

    taboo_rules = [
        "底层概念不破金身：已确立的脑洞公理（如'反向打钱'或'情绪具象化'）不可无预警吃设定，世界所有互动必须严格服从该公理。",
        "逻辑悖论反噬：若概念设定推导出的逻辑自相矛盾，系统与施法者必受因果反噬重创。",
        "闭环演绎守恒：任何概念能力爆发必须交代其波及效应与社会推演，不可写出悬浮无后果的开挂。",
    ]

    travel_speed_limits = {
        "WALK": 60.0,
        "CAR": 1000.0,
        "CONCEPT_JUMP": 80000.0,  # 概念跳跃
        "DIMENSION_FOLD": 999999.0,
    }

    banned_words = [
        "平平无奇套路", "毫无新意",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(BrainHoleGenreDriver())
