# -*- coding: utf-8 -*-
"""
Republic of China Era & Espionage Genre Driver
Covers early 20th century warlord conflicts, concession enclaves, underground espionage,
cipher codes, dead drops, interrogation rooms, and tumultuous patriotic resistance.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class RepublicEraGenreDriver(BaseGenreDriver):
    genre_id = "REPUBLIC_ERA"
    genre_name = "民国风云与谍战暗战 (Republic of China & Espionage)"
    description = "以租界十里洋场、军阀割据混战、地下单线联系、密码电报密战与救亡图存为核心的世界观。"

    power_levels = [
        "租界包探/热血青年志士",
        "军统中尉/地下交通站情报员",
        "情报科长/宪兵特高课顾问/主力团长",
        "省党部站长/野战军长/军阀首席幕僚",
        "特别委员会巨头/战区总司令/谍战破译泰斗",
    ]

    currencies = [
        "袁大头/龙洋银元 (Silver Dollars)",
        "小黄鱼/大黄鱼金条 (Gold Bars)",
        "法币/伪中储券 (Republic Fiat Currency)",
        "各方特许通行证/良民证 (Travel Passes)",
        "密电码本与潜伏名单 (Cipher Books & Personnel Lists)",
    ]

    taboo_rules = [
        "电报与无线电测向真实物理：发报超过三分钟必遭日伪测向车精准定位，严禁无线全天候即时联络。",
        "严禁现代科技穿越穿帮：禁止出现手机、互联网、人脸识别或GPS卫星定位。",
        "地下工作单线联系原则：上下线之间严格执行死信箱与暗号接头，绝不可横向互相知晓全部真实身份。",
        "热兵器火力与生理极限：凡人肉身被毛瑟驳壳枪或汤姆逊扫中必丧失战力，绝无金钟罩肉身挡子弹。",
    ]

    travel_speed_limits = {
        "WALK": 40.0,
        "RICKSHAW": 80.0,      # 人力黄包车
        "STEAM_TRAIN": 600.0,   # 蒸汽机车
        "MILITARY_JEEP": 500.0,
        "STEAM_SHIP": 400.0,
        "PROP_PLANE": 3000.0,   # 螺旋桨客机
    }

    banned_words = [
        "手机", "微信", "电脑", "互联网", "激光", "核聚变", "灵石", "金丹", "飞剑",
    ]

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


register_genre(RepublicEraGenreDriver())
