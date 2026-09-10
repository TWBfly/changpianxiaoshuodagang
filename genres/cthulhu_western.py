# -*- coding: utf-8 -*-
"""
Cthulhu Mythos & Eldritch Fantasy Genre Driver
Covers Victorian steampunk settings, Beyonder potion sequences (序列魔药),
sanity collapse, sealed artifacts with severe penalties, and eldritch horror.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class CthulhuWesternGenreDriver(BaseGenreDriver):
    genre_id = "CTHULHU_WESTERN"
    genre_name = "克苏鲁与诡秘奇幻 (Cthulhu Mythos & Eldritch Fantasy)"
    description = "以维多利亚蒸汽时代、秘偶魔药序列、理智值崩溃、封印物负面代价与不可名状神祇为核心的世界观。"

    power_levels = [
        "普通人/神秘学调查员",
        "中低序列超凡者 (序列9 - 序列7)",
        "中高序列超凡者/秘偶大师 (序列6 - 序列5)",
        "半神圣者/神使巨头 (序列4 - 序列3)",
        "从神天使/大主教 (序列2 - 序列1)",
        "真神主宰/旧日支配者/外神 (序列0 / 旧日)",
    ]

    currencies = [
        "金镑/苏勒/便士 (Pounds, Shillings & Pence)",
        "非凡特性与高阶魔药主材料 (Beyonder Characteristics)",
        "各教会圣堂功勋符咒 (Church Contribution)",
        "高危封印物借用契约 (Sealed Artifact Contracts)",
    ]

    taboo_rules = [
        "不可直视神：凡人凡体直视神祇真身或聆听呓语必瞬间异化为扭曲怪物，不可豁免。",
        "非凡特性不灭定律：非凡特性不会凭空产生也不会毁灭，仅在宿主间转移与聚合。",
        "封印物负面代价强制生效：使用任何超凡遗留物必承担残酷负面代偿，绝无零代价免费神器。",
        "占卜与反向注视法则：窥视更高序列隐秘，必触发高位存在的反向精神污染与锁定。",
    ]

    travel_speed_limits = {
        "WALK": 40.0,
        "CARRIAGE": 80.0,
        "STEAM_TRAIN": 500.0,
        "STEAM_SHIP": 350.0,
        "SPIRIT_WORLD_TRAVERSAL": 50000.0,  # 灵界穿梭/旅行家传送
        "ASTRAL_PROJECTION": 999999.0,
    }

    banned_words = [
        "灵石", "筑基", "大乘期", "修真者", "雷劫", "仙尊", "宗门",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(CthulhuWesternGenreDriver())
