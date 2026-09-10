# -*- coding: utf-8 -*-
"""
Sci-Fi, Cyberpunk & Interstellar Mecha Genre Driver
Covers cybernetic augmentations, cyberpsychosis, starship battles,
Dyson swarms, relativistic physics, and dystopian megacorporations.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class SciFiCyberGenreDriver(BaseGenreDriver):
    genre_id = "SCI_FI_CYBER"
    genre_name = "科幻未来与赛博星际 (Sci-Fi, Cyberpunk & Interstellar)"
    description = "以巨型垄断企业、神经机械义体、赛博精神病、星舰跃迁与热力学能量守恒为核心的世界观。"

    power_levels = [
        "底层生化耗材/未改造原生人",
        "街头黑客/二代军规义体雇佣兵",
        "重型机甲王牌机师/深空巡洋舰长",
        "泰坦歼星舰指挥官/基因星神原体",
        "行星级戴森球主脑/跨星系文明领袖",
        "高维降维打击神级文明",
    ]

    currencies = [
        "星际通用信用点 (Universal Credits)",
        "高浓度反物质能源块 (Antimatter Cells)",
        "超导体与重稀土矿石 (Superconductor Ores)",
        "特权军规芯片加密协议 (Military Neural Chips)",
        "空间跳跃跃迁配额 (FTL Jump Quotas)",
    ]

    taboo_rules = [
        "赛博精神病与算力负荷：肉体义体化程度越高，对大脑神经突触的侵蚀越严重，必须有免疫抑制剂或意志力门槛。",
        "物理与能量守恒定律：歼星轨道炮击必须计算散热峰值与反作用力缓冲，不存在无限零过热连发。",
        "光速与相对论时延：在无曲率引擎或量子纠缠信道下，深空通讯遵循光速延迟限制。",
    ]

    travel_speed_limits = {
        "WALK": 60.0,
        "HOVER_CAR": 2000.0,
        "ORBITAL_SHUTTLE": 30000.0,
        "STARSHIP_SUBLIGHT": 300000.0,
        "WARP_DRIVE": 99999999.0,  # 曲率跃迁
    }

    banned_words = [
        "修真", "灵根", "金丹", "元婴", "天劫", "飞升",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(SciFiCyberGenreDriver())
