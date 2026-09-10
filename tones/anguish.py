# -*- coding: utf-8 -*-
"""
Anguish & Heartache Emotional Tone Driver
Focuses on emotional rupture, tragic miscommunication, irreversible sacrifices,
crematorium regret, and profound psychological ache.
"""

from __future__ import annotations

from typing import Any
from .base_tone import BaseToneDriver, register_tone


class AnguishToneDriver(BaseToneDriver):
    tone_id = "ANGUISH"
    tone_name = "虐文痛感 (Anguish / Heartache / Tragic Misunderstanding)"
    description = "以立场错位、真相迟到、情感撕裂、不可逆遗憾与追悔莫及为核心的情绪基调。"

    tension_curve = "TRAGIC_EROSION"
    max_oppression_beats = 6

    required_emotional_payoffs = [
        "真相大白却为时已晚", "追悔莫及跪地呕血", "至亲割裂剖心以证", "不可逆的情感伤痕", "物是人非雪夜独行"
    ]

    forbidden_tone_tropes = [
        "廉价大团圆金手指瞬间抚平",
        "毫无代价的轻松原谅",
        "死而复生消解全部悲剧重量",
        "毫无情感波动的冷血工具人",
    ]

    dialogue_flavor = [
        "这一剑是我欠你的，如今因果两清，来世莫再相逢。",
        "你若早知今日，又何必当初逼我走上绝路？",
        "我把命都赔给你了，你到底还要我怎样……",
        "当年风雪漫天，你在城楼之上看我万箭穿心，可曾有过半点悔意？",
    ]

    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        full_text = str(chapter_payload)
        violations.extend(self.check_forbidden_tropes(full_text))
        return violations


register_tone(AnguishToneDriver())
