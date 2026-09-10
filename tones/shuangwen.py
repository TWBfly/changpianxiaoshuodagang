# -*- coding: utf-8 -*-
"""
Shuangwen (Power Fantasy & Catharsis) Emotional Tone Driver
Focuses on fast-paced positive feedback, dimension-reduction counterstrikes,
satisfying face-slaps, audience awe, and strict zero-prolonged-humiliation.
"""

from __future__ import annotations

from typing import Any
from .base_tone import BaseToneDriver, register_tone


class ShuangwenToneDriver(BaseToneDriver):
    tone_id = "SHUANGWEN"
    tone_name = "爽文 (Cool & Cathartic Power Fantasy)"
    description = "以快速正反馈闭环、极致打脸反转、丰厚资源收益与全场震撼为核心的情绪基调。"

    tension_curve = "FAST_CATHARSIS"
    max_oppression_beats = 2

    required_emotional_payoffs = [
        "打脸反转", "降维打击", "全场震撼", "收获神级宝物", "果断斩草除根", "反杀逆转"
    ]

    forbidden_tone_tropes = [
        "甘心受辱不思反击",
        "圣母心泛滥放虎归山",
        "惨胜如败颗粒无收",
        "核心道侣遭无端玷污",
        "长期无力吃瘪窝囊",
    ]

    dialogue_flavor = [
        "就凭你，也配审判本尊？",
        "跳梁小丑，井底之蛙，焉知天地之广阔！",
        "今日让你见识何为真正的绝望！",
        "杀你，何须三招？一指足矣！",
    ]

    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)

        # 1. Forbidden tropes check
        violations.extend(self.check_forbidden_tropes(full_text))

        # 2. Prolonged unavenged oppression check
        beats = chapter_payload.get("dynamic_beats", [])
        if isinstance(beats, list):
            oppression_run = 0
            for idx, b in enumerate(beats):
                if not isinstance(b, dict):
                    continue
                role = b.get("beat_role", "")
                action = b.get("action", "")
                cf = b.get("counterforce", "")
                # If beat describes pure humiliation/suppression without active counterplay
                if any(w in cf for w in ("凌辱", "践踏", "重创垂死", "绝望无力")) and not any(
                    w in action for w in ("冷笑", "暗中", "留后手", "布局", "反杀", "底牌", "爆发")
                ):
                    oppression_run += 1
                else:
                    oppression_run = 0

                if oppression_run > self.max_oppression_beats:
                    violations.append(
                        f"Ch {c_no} Beat {idx+1}: Excessive prolonged passive oppression ({oppression_run} beats) violates Shuangwen tone."
                    )

        return violations


register_tone(ShuangwenToneDriver())
