# -*- coding: utf-8 -*-
"""
Game System & Fourth Calamity Genre Driver
Covers virtual reality MMOs, e-sports competition, Lord building (领主基建),
Fourth Calamity player sociology, and numerical character attributes.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class GameSystemGenreDriver(BaseGenreDriver):
    genre_id = "GAME_SYSTEM"
    genre_name = "游戏竞技与第四天灾 (Game System & Fourth Calamity)"
    description = "以严密数值面板、职业转职分支、领地基建扩张、玩家群体行为学与战役副本为核心的世界观。"

    power_levels = [
        "LV.1 萌新白板/普通村民",
        "LV.20 进阶一转职业/领地骑士",
        "LV.50 觉醒二转专家/封地男爵",
        "LV.80 传奇转职/公会会长/王国大公",
        "LV.100 神话巅峰/世界首杀巨头/第四天灾领袖",
    ]

    currencies = [
        "游戏金币/银币 (In-game Gold/Silver)",
        "未分配自由属性点 (Stat Points)",
        "公会战功贡献度 (Guild Contribution)",
        "领地四维基础资源：石料/木材/铁矿/粮食 (Raw Resources)",
        "现实货币现金兑换池 (Real Money Exchange)",
    ]

    taboo_rules = [
        "数值与战斗逻辑自洽律：伤害计算必须受防御减伤、抗性判定与攻击力约束，数值不可随心所欲口胡膨胀。",
        "第四天灾玩家社会学：玩家具有逐利、喜好搞事与不可完全奴役性，NPC发布任务必须符合利益驱动与正负反馈。",
        "系统死亡与惩罚机制：副本死亡掉级、掉装备或复活CD必须严格执行，不可因主角光环凭空取消底层代码限制。",
    ]

    travel_speed_limits = {
        "WALK": 50.0,
        "MOUNT_HORSE": 150.0,
        "FLYING_MOUNT": 1200.0,
        "CITY_PORTAL": 999999.0,  # 主城传送阵
    }

    banned_words = [
        "元婴", "化神", "大乘期", "九幽锁龙",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(GameSystemGenreDriver())
