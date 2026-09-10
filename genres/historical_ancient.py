# -*- coding: utf-8 -*-
"""
Historical & Ancient Dynasty Genre Driver
Covers fictional dynasty building, court political intrigue, feudal warlord conquest,
administrative logistics, imperial examinations, and grand military campaigns.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class HistoricalAncientGenreDriver(BaseGenreDriver):
    genre_id = "HISTORICAL_ANCIENT"
    genre_name = "架空历史与王朝权谋 (Historical Dynasty & Court Politics)"
    description = "以封建官僚政治、士族门阀博弈、冷兵器行军军饷、改朝换代与农桑治国为核心的世界观。"

    power_levels = [
        "布衣白身/秀才举人",
        "县令县丞/七品芝麻官",
        "知府刺史/四品封疆门槛",
        "六部尚书/都御史/总督巡抚",
        "内阁首辅/大将军/顾命重臣",
        "摄政诸侯/开国太祖/九五至尊",
    ]

    currencies = [
        "铜钱文钱 (Copper Coins)",
        "纹银两数 (Silver Taels)",
        "赤金铤锭 (Gold Ingots)",
        "粮食石斗/军饷草料 (Grain & Rations)",
        "两淮盐引/茶马通商文牒 (Salt & Tea Monopolies)",
        "食邑世袭爵位 (Feudal Titles)",
    ]

    taboo_rules = [
        "纯历史冷兵器物理极限：绝无飞剑遁地，单挑无法万人敌，重骑兵与弓弩有严格体力与箭矢损耗。",
        "后勤粮道生命线：大军出征十里转运一石，粮道断绝不出三日全军必自溃。",
        "封建宗族与士绅网络：皇帝无法单凭口谕瞬间废除天下地主土地，必经权力博弈与政令传达周转。",
        "信件通信速度守恒：八百里加急为信息传递极限，不可跨千里实时知悉边关军情。",
    ]

    travel_speed_limits = {
        "WALK": 40.0,
        "HORSE_MESSENGER": 600.0,  # 八百里加急快马换乘
        "HORSE": 120.0,
        "CARRIAGE": 80.0,
        "CANAL_BOAT": 180.0,
        "MARCH_INFANTRY": 50.0,
        "MARCH_CAVALRY": 100.0,
    }

    banned_words = [
        "PPT", "自付50%", "自付", "现代绩效", "大数据", "商业模式", "互联网", "对冲基金",
        "手机", "电脑", "汽车", "飞机", "特警", "医保卡", "反恐",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(HistoricalAncientGenreDriver())
