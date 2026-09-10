# -*- coding: utf-8 -*-
"""
Passionate & Blood-Boiling Emotional Tone Driver
Focuses on unshakable comradeship, soaring defiance, battle hymns,
breaking limits through sheer will, and roaring declarations.
"""

from __future__ import annotations

from typing import Any
from .base_tone import BaseToneDriver, register_tone


class PassionateToneDriver(BaseToneDriver):
    tone_id = "PASSIONATE"
    tone_name = "热血高燃 (Passionate / Blood-Boiling Shonen Defiance)"
    description = "以意志突破极限、同袍生死与共、绝境向死而生与仰天咆哮破局为核心的情绪基调。"

    tension_curve = "PASSIONATE_ROAR"
    max_oppression_beats = 3

    required_emotional_payoffs = [
        "残躯拔刀再次站起", "同袍背靠背生死誓约", "怒吼震碎神魔桎梏", "绝境极限反杀", "燃尽热血照亮黑夜"
    ]

    forbidden_tone_tropes = [
        "利己精算背弃生死挚友",
        "未战先怯抱头鼠窜",
        "冷血麻木对牺牲无动于衷",
        "主角毫无底线屈膝求饶",
    ]

    dialogue_flavor = [
        "我还没死，你们高兴得太早了！再来！！",
        "想动我身后的人，先从我的尸体上踏过去！",
        "这所谓的宿命天意，今日我便一拳将它砸得粉碎！",
        "只要心脏还在跳动，手中的刀就绝不会落下！",
    ]

    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        full_text = str(chapter_payload)
        violations.extend(self.check_forbidden_tropes(full_text))
        return violations


register_tone(PassionateToneDriver())
