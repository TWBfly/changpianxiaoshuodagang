# -*- coding: utf-8 -*-
"""
Suspense & Detective Investigation Genre Driver
Covers forensic criminal investigation, locked-room puzzles, psychological profiling,
legal procedure evidence chains, and strict anti-deus-ex-machina detective rules.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class SuspenseDetectiveGenreDriver(BaseGenreDriver):
    genre_id = "SUSPENSE_DETECTIVE"
    genre_name = "悬疑推理与刑侦破案 (Suspense & Detective Mystery)"
    description = "以严密物证链条、法医病理学、密室逻辑推演、犯罪心理画像与正义程序为核心的世界观。"

    power_levels = [
        "实习警员/业余推理爱好者",
        "重案组骨干/法医师承主检",
        "刑警支队长/现场勘查首席",
        "省厅特聘刑侦专家/首席侧写师",
        "国际刑警高级督察/传奇探长",
    ]

    currencies = [
        "法庭认可铁证 (Admissible Forensic Evidence)",
        "检察院搜查令/通缉令 (Search Warrants)",
        "绝密涉案档案调阅权限 (Classified Dossiers)",
        "污点证人保护协定 (Witness Immunity)",
    ]

    taboo_rules = [
        "诺克斯与范达因黄金法则：凶手必须在前半程已登场人物中产生，严禁终局突兀空降此前未提及的新人。",
        "物理与法医学守恒：死亡时间受尸僵、尸斑、胃溶物严格约束，毒物致死必有靶向生化病理机制。",
        "物证链不可污染：关键物证转移提取必须合法规范，禁止无源头伪造或神秘凭空出现证据。",
        "严禁机械降神与灵媒占卜：侦破必凭人类观察与严密逻辑，禁止特异功能直视凶手名字。",
    ]

    travel_speed_limits = {
        "WALK": 40.0,
        "POLICE_CAR": 1200.0,
        "TRAIN": 3000.0,
        "HELICOPTER": 4000.0,
        "FLIGHT": 12000.0,
    }

    banned_words = [
        "天劫", "元婴", "飞剑", "瞬移", "通灵显圣", "因果金光", "大乘期",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(SuspenseDetectiveGenreDriver())
