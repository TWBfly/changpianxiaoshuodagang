# -*- coding: utf-8 -*-
"""
Suspense & Serious Emotional Tone Driver
Focuses on logical rigor, cold tension, psychological warfare, forensic deduction,
and strict avoidance of comical bathos or deus ex machina.
"""

from __future__ import annotations

from typing import Any
from .base_tone import BaseToneDriver, register_tone


class SuspenseSeriousToneDriver(BaseToneDriver):
    tone_id = "SUSPENSE_SERIOUS"
    tone_name = "悬疑严肃 (Suspense / Noir / Forensic Deduction)"
    description = "以抽丝剥茧的严密证据链、高压心理博弈、真实死亡威胁与冷峻宿命感为核心的情绪基调。"

    tension_curve = "HIGH_TENSION_NOIR"
    max_oppression_beats = 5

    required_emotional_payoffs = [
        "物证证据链闭环", "动机与行凶路径破解", "心理防线彻底瓦解", "伏笔暗线呼应收束", "真相残酷震撼揭晓"
    ]

    forbidden_tone_tropes = [
        "机械降神瞬间破案",
        "凶手弱智无端自爆",
        "生死对峙中无厘头打情骂俏",
        "证据毫无铺垫空中楼阁",
        "主角全知开挂看穿凶手",
    ]

    dialogue_flavor = [
        "你算漏了一件事——当晚城西下过暴雨，而你的鞋底干净得像刚换过一样。",
        "真正的谎言，往往有九成是真的，唯独最关键的那一秒被调换了。",
        "看着我的眼睛，在悬剑司的大牢里，没有人能把秘密带进棺材。",
        "凶手不是外人，他此刻就坐在我们这张谈判桌的对面。",
    ]

    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        full_text = str(chapter_payload)
        violations.extend(self.check_forbidden_tropes(full_text))
        return violations


register_tone(SuspenseSeriousToneDriver())
