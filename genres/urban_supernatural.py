# -*- coding: utf-8 -*-
"""
Urban Supernatural & Cultivation Genre Driver
Covers modern city cultivation, superpower awakening, spiritual reiki recovery,
special investigation bureaus (特勤局/守夜人), and ancient inheritance in modern cities.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class UrbanSupernaturalGenreDriver(BaseGenreDriver):
    genre_id = "URBAN_SUPERNATURAL"
    genre_name = "都市异能与都市修仙 (Urban Supernatural & Modern Cultivation)"
    description = "以现代都市为舞台的异能觉醒、灵气复苏、隐世修仙宗门与隐秘特事局博弈世界观。"

    power_levels = [
        "未觉醒凡人 / 练气学徒",
        "E阶觉醒者 / 筑基真人",
        "D阶破军级 / 金丹宗师",
        "C阶镇城级 / 元婴天尊",
        "B阶灭国级 / 化神老祖",
        "A阶半神级 / 渡劫真圣",
        "S阶星空极道 / 天仙至尊",
    ]

    currencies = [
        "现代合法资金 (RMB/USD)",
        "高纯度灵气晶石 (Reiki Crystal)",
        "特事局战功积分 (Bureau Merit Points)",
        "基因觉醒药剂 (Awakening Serum)",
        "天材地宝黑市筹码 (Black Market Chips)",
    ]

    taboo_rules = [
        "现世保密与社会秩序协议：凡人在闹市目击超自然必有记忆消除或舆情封锁机制。",
        "能级守恒与精神负荷：越阶爆发异能必有脑域刺痛或灵力反噬代价。",
        "热武器与灵力临界点：低阶超凡者无法免疫近距离云爆弹或重炮饱和打击。",
    ]

    travel_speed_limits = {
        "WALK": 60.0,
        "CAR": 1200.0,
        "HIGH_SPEED_RAIL": 4000.0,
        "SUPERNATURAL_FLASH": 8000.0,  # 异能雷闪/踏空
        "FLIGHT": 15000.0,
        "SPATIAL_PORTAL": 999999.0,
    }

    banned_words = [
        "PPT", "自付50%", "KPI", "大数据报表", "医保卡",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(UrbanSupernaturalGenreDriver())
