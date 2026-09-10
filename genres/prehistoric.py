# -*- coding: utf-8 -*-
"""
Prehistoric Mythos & Tribulation Genre Driver (洪荒神话 / 封神西游)
Enforces:
- Heavenly Dao destiny and Kalpa (量劫) cycles.
- Sage karma game board (圣人之下皆蝼蚁，大势不可改，小势可改).
- Merit and Negative Karma balance (功德 vs 业力).
- Innate Spiritual Treasures (先天灵宝) suppression tiers.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class PrehistoricGenreDriver(BaseGenreDriver):
    genre_id = "HONGHUANG"
    genre_name = "洪荒神话与无量量劫 (Prehistoric Mythos & Tribulation)"
    description = "以盘古开天、天道大势、圣人棋局、无量量劫、功德业力与先天至宝为核心的世界观。"

    power_levels = [
        "地仙 / 天仙 (Earth / Heaven Immortal)",
        "真仙 / 玄仙 (True / Mystic Immortal)",
        "金仙 (Golden Immortal - Inextinguishable Body)",
        "太乙金仙 (Taiyi Golden Immortal - Five Qi Assembly)",
        "大罗金仙 (Daluo Golden Immortal - Beyond Fate & River of Time)",
        "准圣 / 混元金仙 (Quasi-Sage - Severing Three Corpses)",
        "混元大罗金仙 / 天道圣人 (Saint of Heavenly Dao - Omnipresent)",
        "天道合道者 (Heavenly Dao Harmonizer)",
    ]

    currencies = [
        "九天功德金光 (Merit Golden Light)",
        "气运龙脉 (Providential Luck)",
        "先天不灭灵光 (Innate Indestructible Light)",
        "混沌紫气 (Primordial Purple Qi)",
        "业力红莲焚煞 (Karmic Sin Fire)",
    ]

    taboo_rules = [
        "【大势刚性律】天道大势不可逆（如巫妖必陨、商周必变、佛法必东渡），强逆天道大势者必遭九天神雷劫灰飞烟灭；唯微观小势与人道生灵命运可改。",
        "【圣人无量因果】圣人万劫不磨，金仙难伤分毫；凡向圣人出手必借先天至宝（诛仙阵/太极图/盘古幡）或众生愿力大阵。",
        "【因果业力守恒】凡杀生破戒必沾染红尘杀劫与红莲业力，业力深重者逢量劫必上封神榜或化作劫灰。",
        "【大罗跳出时空】大罗金仙跳出三界外、不在五行中，过去未来一念通达，凡俗物理时空无法束缚其神念。",
    ]

    travel_speed_limits = {
        "WALK": 100.0,
        "CLOUD_RIDE": 5000.0,         # 腾云驾雾
        "EARTH_ESCAPE": 10000.0,       # 地遁神光
        "JIN_DOU_CLOUD": 108000.0,     # 筋斗云 (十万八千里)
        "DALUO_TEAR_VOID": 9999999.0,  # 大罗撕裂虚空
    }

    banned_words = [
        "PPT", "自付50%", "现代绩效", "反恐", "商业路演", "主神空间", "基因锁",
        "医保卡", "股票", "投行",
    ]

    institutional_translations = {
        "朝廷": "殷商王庭 / 大周宗周",
        "内阁/议会": "紫霄宫议事 / 封神大典群仙定榜",
        "公司": "阐截二教道场 / 西方极乐净土",
    }

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)

        # Check immersion lexicon
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")

        # Check Karma & Treasure hierarchy
        beats = chapter_payload.get("dynamic_beats", [])
        for idx, b in enumerate(beats):
            action = b.get("action", "")
            if "圣人" in action and any(k in action for k in ("诛杀", "斩杀", "击杀", "消灭")):
                counter = b.get("counterforce", "")
                if not any(k in counter for k in ("至宝", "天道", "代价", "封神", "气运", "反噬", "大阵")):
                    violations.append(
                        f"Ch {c_no} Beat {idx+1}: Saint killed or subdued without supreme Karma/Tribulation or Innate Treasure."
                    )

        return violations


register_genre(PrehistoricGenreDriver())
