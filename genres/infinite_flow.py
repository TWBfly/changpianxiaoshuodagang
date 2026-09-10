# -*- coding: utf-8 -*-
"""
Infinite Flow & Multiverse Genre Driver (无限流 / 诸天轮回)
Enforces:
- Main God / Samsara Hub point economy.
- Worldview law rejection (tech weapons in magic realms, magic in sci-fi realms).
- Obliteration countdowns and team survival game theory.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class InfiniteFlowGenreDriver(BaseGenreDriver):
    genre_id = "INFINITE_FLOW"
    genre_name = "诸天无限流 (Infinite Flow & Multiverse)"
    description = "以主神空间任务、跨位面世界观排斥、积分强化树、死亡淘汰制与团战博弈为核心的世界观。"

    power_levels = [
        "初阶轮回者 (Tier 1: Novice / Single Skill)",
        "资深求生者 (Tier 2: Veteran / Hybrid Core)",
        "基因锁三阶/觉醒者 (Tier 3: Awakened Strategist)",
        "领域/队长级 (Tier 4: Realm Master / Team Leader)",
        "半神/破格级 (Tier 5: Transcendent Bug Exploit)",
        "主神执政官/观察者 (Tier 6: Arbiter)",
    ]

    currencies = [
        "主神轮回积分 (Reward Points)",
        "支线剧情徽章 (Plot Badges - D/C/B/A/S)",
        "位面本源碎片 (Origin Shards)",
        "免疫抹杀符 (Obliteration Exemption Token)",
    ]

    taboo_rules = [
        "【位面法则排斥律】高科技精密仪器进入高浓度灵力/魔幻位面必受电磁/法则干扰而精度衰减；修真者进入末法科技位面真元不可自然补充。",
        "【主神抹杀悬刃】主线任务倒计时归零或离开任务边界超过限定距离，主神直接执行不可抗拒之抹杀惩罚。",
        "【信息封口令】严禁向土著剧情人物主动泄露主神空间与剧透现实，违者扣除大量积分或直接抹杀。",
        "【负和团战博弈】不同轮回小队进入同一阵营对抗位面，杀戮对方成员获得积分，团灭队伍获得其全部遗产。",
    ]

    travel_speed_limits = {
        "WALK": 50.0,
        "VEHICLE": 800.0,
        "SUB_LIGHT_FLIGHT": 50000.0,
        "SPACE_WARP": 9999999.0,     # 主神传送光柱
    }

    banned_words = [
        "天下第一师门", "七位绝色师姐", "奉天靖难", "满朝文武", "长公主登基",
    ]

    institutional_translations = {
        "朝廷/官府": "位面联邦执政议会 / 本土防卫军",
        "江湖门派": "轮回开拓者公会 / 觉醒者俱乐部",
        "皇帝": "位面世界意识意志 / 空间首席仲裁者",
    }

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)

        # Check immersion lexicon
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")

        # Check Mission & Point economy integrity
        beats = chapter_payload.get("dynamic_beats", [])
        if not isinstance(beats, list):
            return violations
        for idx, b in enumerate(beats):
            if not isinstance(b, dict):
                continue
            action = b.get("action", "")
            if "强化" in action or "兑换" in action:
                counter = b.get("counterforce", "")
                if not any(k in counter for k in ("积分", "支线", "代价", "负荷", "徽章", "扣除")):
                    violations.append(
                        f"Ch {c_no} Beat {idx+1}: Hub enhancement without Reward Point/Plot Badge deduction cost."
                    )

        # Check Realm Law Friction
        realm_mode = chapter_payload.get("realm_mode", "")
        if realm_mode in {"HISTORICAL", "CULTIVATION", "ANCIENT"}:
            for idx, b in enumerate(beats):
                if not isinstance(b, dict):
                    continue
                act = b.get("action", "")
                if any(tech in act for tech in ("智能手机", "维基百科", "核弹", "步枪", "互联网", "导弹")):
                    violations.append(
                        f"Ch {c_no} Beat {idx+1}: Anachronistic element violates realm law friction in {realm_mode} realm."
                    )

        return violations


register_genre(InfiniteFlowGenreDriver())
