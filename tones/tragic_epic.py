# -*- coding: utf-8 -*-
"""
Tragic Epic & Heroic Sacrifice Emotional Tone Driver
Focuses on sublime sacrifice, unyielding resistance against insurmountable odds,
civilizational torch passing, and monumental existential weight.
"""

from __future__ import annotations

from typing import Any
from .base_tone import BaseToneDriver, register_tone


class TragicEpicToneDriver(BaseToneDriver):
    tone_id = "TRAGIC_EPIC"
    tone_name = "悲壮史诗 (Tragic Epic & Heroic Sacrifice)"
    description = "以明知必死而决然赴之、慷慨守城、薪火不绝与以凡人之躯抗衡天倾为核心的情绪基调。"

    tension_curve = "SACRIFICIAL_HYMN"
    max_oppression_beats = 5

    required_emotional_payoffs = [
        "以命填山海", "断剑长插界碑永不后退", "薪火与意志传承", "百万英魂共赴国难", "天崩地裂一人独挡"
    ]

    forbidden_tone_tropes = [
        "嬉皮笑脸消解崇高感",
        "主角或领袖贪生怕死逃跑",
        "廉价复活抵消壮烈牺牲",
        "庸俗算计破坏史诗悲鸣",
    ]

    dialogue_flavor = [
        "大玄三百年国祚，未有退缩之天子，亦无屈膝之守将！",
        "身后便是锦绣山河、父老妻儿，退无可退，唯有拔刀死战！",
        "借这人间三尺剑，敢教日月换新天！诸君，随我冲锋！",
        "我们若不死在今夜，后世子孙便永远跪在深渊之中！",
    ]

    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        full_text = str(chapter_payload)
        violations.extend(self.check_forbidden_tropes(full_text))
        return violations


register_tone(TragicEpicToneDriver())
