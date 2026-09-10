# -*- coding: utf-8 -*-
"""
Xianxia & Xuanhuan Genre Driver
Implements cultivation realms, spirit stone economy, pill/herb alchemy,
immersion translation, and power-tier suppression constraints.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class XianxiaGenreDriver(BaseGenreDriver):
    genre_id = "XIANXIA"
    genre_name = "传统修真与东方玄幻 (Xianxia & Xuanhuan)"
    description = "以境界修持、宗门神权、灵石丹药、飞升天梯与天道因果为核心的世界观。"

    power_levels = [
        "练气期 (Qi Refining)",
        "筑基期 (Foundation Establishment)",
        "金丹期 (Golden Core)",
        "元婴期 (Nascent Soul)",
        "化神期 (Soul Formation)",
        "炼虚期 (Void Refinement)",
        "合体期 (Body Integration)",
        "大乘期 (Great Ascension)",
        "渡劫期 (Tribulation Crossing)",
        "真仙境 (True Immortal)",
    ]

    currencies = [
        "下品灵石 (Low-grade Spirit Stone)",
        "中品灵石 (Mid-grade Spirit Stone)",
        "上品灵石 (High-grade Spirit Stone)",
        "极品灵晶 (Top-grade Spirit Crystal)",
        "宗门功勋点 (Sect Merit Points)",
        "寿元丹 (Lifespan Extension Pill)",
    ]

    taboo_rules = [
        "大境界不可无代价逆伐：凡人/练气绝不可无损秒杀高阶修士，跨阶必付本命寿元或神兵折损代价。",
        "神识与传音遵循物理距离与禁制阻隔，不可全知瞬通。",
        "杀生夺宝必结因果，心魔劫数不可避免。",
        "灵石与法力物理守恒，高阶法阵必有灵脉或灵晶消耗支撑。",
    ]

    travel_speed_limits = {
        "WALK": 60.0,
        "HORSE": 150.0,
        "CARRIAGE": 100.0,
        "SPIRIT_BOAT": 800.0,       # 飞舟
        "FLY_SWORD": 2500.0,        # 御剑飞行
        "TELEPORT_ARRAY": 100000.0, # 跨洲传送阵
    }

    banned_words = [
        "PPT", "自付50%", "自付", "蒙古族", "反恐", "现代绩效", "五大洋",
        "现代分权", "医保卡", "自鸣钟", "炸膛", "盲审重考", "假模范县", "共济渠",
        "KPI", "大数据", "商业模式", "互联网", "对冲基金",
    ]

    institutional_translations = {
        "PPT": "虚饰文牍图谱",
        "报表": "政绩账册",
        "反恐": "缉凶平暴",
        "医保": "百草济民堂公费补贴",
        "绩效考核": "考成法铁律考评",
        "分权制衡": "三省六部议政分权",
        "商业保险": "万宝安平互保会",
        "高利贷": "九出十三归印子钱",
        "特警": "悬剑司重装缉捕鹰犬",
    }

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)

        # Check immersion lexicon
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")

        # Check cost realism: high breakthrough must carry real cost
        beats = chapter_payload.get("dynamic_beats", [])
        if not isinstance(beats, list):
            return violations

        ch_has_breakthrough = False
        ch_cost_text = ""
        for idx, b in enumerate(beats):
            if not isinstance(b, dict):
                continue
            action = b.get("action", "")
            beat_text = f"{action} {b.get('counterforce', '')} {b.get('new_information_or_choice', '')} {str(b.get('delta', ''))}"
            ch_cost_text += " " + beat_text
            # Check if this beat is an accomplished cultivation breakthrough
            if ("连破三阶" in action or "突破至" in action or "境界突破" in action or "修为突破" in action) and "企图" not in action:
                ch_has_breakthrough = True

        if ch_has_breakthrough:
            cost_keywords = ("雷劫", "心魔", "吐血", "代价", "虚弱", "损耗", "裂纹", "负伤", "昏睡", "限制", "剧痛", "经脉", "疲惫", "透支")
            if not any(kw in ch_cost_text for kw in cost_keywords):
                violations.append(f"Ch {c_no}: Cultivation breakthrough lacks required tribulation/cost across chapter beats.")

        return violations


register_genre(XianxiaGenreDriver())
