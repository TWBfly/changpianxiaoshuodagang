# -*- coding: utf-8 -*-
"""
Genres package: exposes BaseGenreDriver, dynamic genre creators, and all concrete drivers.
"""

from __future__ import annotations

from .base_driver import (
    BaseGenreDriver,
    get_genre_driver,
    list_registered_genres,
    register_genre,
)
from .dynamic_genre import (
    CustomDynamicGenreDriver,
    create_custom_genre,
)
from .xianxia import XianxiaGenreDriver
from .horror import HorrorGenreDriver
from .infinite_flow import InfiniteFlowGenreDriver
from .prehistoric import PrehistoricGenreDriver
from .urban_realistic import UrbanRealisticGenreDriver
from .urban_supernatural import UrbanSupernaturalGenreDriver
from .historical_ancient import HistoricalAncientGenreDriver
from .suspense_detective import SuspenseDetectiveGenreDriver
from .brain_hole import BrainHoleGenreDriver
from .republic_era import RepublicEraGenreDriver
from .cthulhu_western import CthulhuWesternGenreDriver
from .sci_fi_cyber import SciFiCyberGenreDriver
from .game_system import GameSystemGenreDriver

HonghuangGenreDriver = PrehistoricGenreDriver

__all__ = [
    "BaseGenreDriver",
    "get_genre_driver",
    "list_registered_genres",
    "register_genre",
    "CustomDynamicGenreDriver",
    "create_custom_genre",
    "XianxiaGenreDriver",
    "HorrorGenreDriver",
    "InfiniteFlowGenreDriver",
    "PrehistoricGenreDriver",
    "HonghuangGenreDriver",
    "UrbanRealisticGenreDriver",
    "UrbanSupernaturalGenreDriver",
    "HistoricalAncientGenreDriver",
    "SuspenseDetectiveGenreDriver",
    "BrainHoleGenreDriver",
    "RepublicEraGenreDriver",
    "CthulhuWesternGenreDriver",
    "SciFiCyberGenreDriver",
    "GameSystemGenreDriver",
]
