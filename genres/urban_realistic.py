# -*- coding: utf-8 -*-
"""
Urban Realistic Genre Driver
Covers modern business war, workplace promotion, tycoon/godly doctor,
financial markets, legal compliance, and realistic social physics.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class UrbanRealisticGenreDriver(BaseGenreDriver):
    genre_id = "URBAN_REALISTIC"
    genre_name = "都市现实与商战职场 (Urban Realistic & Business)"
    description = "以现代商业社会、职场升迁、金融杠杆、神医医道、社会声望与法律秩序为核心的世界观。"

    power_levels = [
        "底层职员/见习学徒",
        "业务骨干/部门主管",
        "行业新锐/分公司高管",
        "独角兽创始人/资本合伙人",
        "产业巨头/百亿集团董事",
        "跨国财阀领袖/金融托拉斯幕后操盘手",
    ]

    currencies = [
        "人民币 (RMB)",
        "美元 (USD)",
        "公司股份/期权 (Equity & Stock Options)",
        "政商名流人脉契约 (Social Capital)",
        "顶级信贷授信额度 (Credit Line)",
    ]

    taboo_rules = [
        "现代物理法则绝对生效：凡人不能肉身抗反器材狙击枪或违背重力飞行。",
        "金融与资本守恒：百亿资金调动必须有银行监管清算与审计逻辑，不可无中生有印钞。",
        "公权力与国家机器威严：不可在现代一线闹市大规模无后果屠杀平民。",
        "现代医学客观规律：针灸与医道不可凭空让完全脑死亡三日者原地复活。",
    ]

    travel_speed_limits = {
        "WALK": 50.0,
        "SUBWAY_BUS": 300.0,
        "CAR": 1200.0,
        "HIGH_SPEED_RAIL": 4000.0,
        "COMMERCIAL_FLIGHT": 12000.0,
        "PRIVATE_JET": 16000.0,
    }

    banned_words = [
        "金丹", "元婴", "筑基", "大乘期", "洞天福地", "御剑飞行", "九幽锁龙", "天道誓言",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(UrbanRealisticGenreDriver())
