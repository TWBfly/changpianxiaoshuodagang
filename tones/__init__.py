# -*- coding: utf-8 -*-
"""
Tones Package
Exposes tone drivers, registry functions, and dynamic tone creation factory.
"""

from __future__ import annotations

from .base_tone import (
    BaseToneDriver,
    register_tone,
    get_tone_driver,
    list_registered_tones,
    create_custom_tone,
    CustomDynamicToneDriver,
)
from .shuangwen import ShuangwenToneDriver
from .humor import HumorToneDriver
from .suspense_serious import SuspenseSeriousToneDriver
from .anguish import AnguishToneDriver
from .tragic_epic import TragicEpicToneDriver
from .passionate import PassionateToneDriver

__all__ = [
    "BaseToneDriver",
    "register_tone",
    "get_tone_driver",
    "list_registered_tones",
    "create_custom_tone",
    "CustomDynamicToneDriver",
    "ShuangwenToneDriver",
    "HumorToneDriver",
    "SuspenseSeriousToneDriver",
    "AnguishToneDriver",
    "TragicEpicToneDriver",
    "PassionateToneDriver",
]
