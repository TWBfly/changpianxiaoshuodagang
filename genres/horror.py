# -*- coding: utf-8 -*-
"""
Urban Horror & Rules-Based Weirdness Genre Driver (都市异能 / 规则怪谈 / 诡异流)
Enforces:
- Inviolable rules: Ghosts cannot be physically killed, only countered by rules.
- Sanity (San) points / mental corruption entropy.
- Curse compensation (every supernatural power costs life or body parts).
- Investigation-driven survival deductions.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class HorrorGenreDriver(BaseGenreDriver):
    genre_id = "HORROR"
    genre_name = "都市异能与规则怪谈 (Urban Horror & Rules-based Weirdness)"
    description = "以不可知诡异、规则怪谈、San值侵蚀、封印代偿与绝境智斗求生为核心的世界观。"

    power_levels = [
        "普通调查员 (Civilian Investigator)",
        "知悉者 (Aware / San 80-100)",
        "契约者 (Contractor / San 60-80)",
        "融诡者 (Specter Fusion / San 40-60)",
        "异化执灯人 (Alienated Keeper / San 20-40)",
        "诡异源头/不可名状 (Calamity Source / San 0)",
    ]

    currencies = [
        "理智值 (Sanity Points)",
        "鬼烛 (Ghost Candle - Burn Time)",
        "诡钞 (Nethernotes)",
        "替死符/替死草人 (Substitution Totem)",
        "封印物收容代偿时限 (Containment Grace Period)",
    ]

    taboo_rules = [
        "【第一诡异铁律】鬼怪与不可名状存在绝无法被纯物理伤害杀死（枪炮、刀剑无伤），只能以规则对抗规则，或借用诡异代偿封印。",
        "【第二侵蚀铁律】动用诡异之力必遭不可逆污染或寿命代偿（身体石化、内脏枯竭、剥夺五感等）。",
        "【第三杀人规律铁律】每个怪谈必定严格遵照其杀人规律触发，只要完全遵守生路规则，弱者亦可规避抹杀。",
        "【第四信息封锁铁律】官方异常局对普通大众维持信息茧房，泄露必引发社会恐慌污染扩散。",
    ]

    travel_speed_limits = {
        "WALK": 40.0,
        "SUBWAY": 400.0,
        "CAR": 600.0,
        "SPECIAL_FLIGHT": 2000.0,
        "GHOST_REALM_SHIFT": 10000.0, # 鬼蜮空间跳跃 (消耗巨大San值)
    }

    banned_words = [
        "御剑飞行", "金丹", "元婴", "飞升", "洪荒大劫", "圣人果位",
        "一剑开天门", "纯阳仙气", "灵石", "宗门大比",
    ]

    institutional_translations = {
        "衙门": "市特别调查事务局",
        "江湖宗门": "民间隐秘结社/收容俱乐部",
        "捕快": "异常收容特遣队员",
        "掌教/宗主": "首席收容研究长",
        "法宝": "特异封印禁忌物",
    }

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)

        # Check immersion lexicon
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")

        # Check Taboo 1: Ghosts cannot be physically crushed by pure brute force
        beats = chapter_payload.get("dynamic_beats", [])
        if not isinstance(beats, list):
            return violations
        for idx, b in enumerate(beats):
            if not isinstance(b, dict):
                continue
            action = b.get("action", "")
            if any(term in action for term in ("一拳轰杀厉鬼", "剑斩不可名状", "肉身将鬼打爆", "无伤秒杀怪谈", "砍死红衣厉鬼", "砍死厉鬼", "杀死厉鬼", "消灭厉鬼")):
                violations.append(
                    f"Ch {c_no} Beat {idx+1}: Violates Horror Taboo 1 - Mortal physical weapons cannot permanently kill an entity, only rules and containment work."
                )

            # Check Cost: Using supernatural power must mention sanity or physical corruption
            if "动用诡异" in action or "动用封印物" in action:
                counter = b.get("counterforce", "")
                if not any(k in counter for k in ("San", "理智", "侵蚀", "代价", "枯竭", "污染", "反噬", "替死")):
                    violations.append(
                        f"Ch {c_no} Beat {idx+1}: Supernatural usage without Sanity loss or physical curse cost."
                    )

        return violations


register_genre(HorrorGenreDriver())
