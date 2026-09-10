# -*- coding: utf-8 -*-
"""
Humor & Comedy Emotional Tone Driver
Focuses on comic misunderstandings, bathos (deflating pretentiousness),
expectation inversion, witty roasts, and unhinged brain-hole logic.
"""

from __future__ import annotations

from typing import Any
from .base_tone import BaseToneDriver, register_tone


class HumorToneDriver(BaseToneDriver):
    tone_id = "HUMOR"
    tone_name = "幽默搞笑 (Humor / Comedy / Bathos)"
    description = "以反差萌、逼格碎裂、迪化误会、无厘头反转与欢快吐槽为核心的情绪基调。"

    tension_curve = "COMIC_INVERSION"
    max_oppression_beats = 4

    required_emotional_payoffs = [
        "逼格瞬间碎裂", "戏剧性误解加深", "一本正经胡说八道", "受害者反向打钱", "全员迪化脑补", "啼笑皆非逆转"
    ]

    forbidden_tone_tropes = [
        "苦大仇深全篇压抑",
        "严肃居高临下说教",
        "沉闷毫无包袱反转",
        "主角无趣死板冷血",
    ]

    dialogue_flavor = [
        "这届反派不太行啊，演戏能不能专业点？",
        "我本想以普通人的身份跟你们相处，可换来的却是加钱？",
        "别脑补了！我真的只是手滑点错了！",
        "大师，收收神通吧，隔壁宗门裤衩子都被你忽悠没了！",
    ]

    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        full_text = str(chapter_payload)
        violations.extend(self.check_forbidden_tropes(full_text))
        return violations


register_tone(HumorToneDriver())
