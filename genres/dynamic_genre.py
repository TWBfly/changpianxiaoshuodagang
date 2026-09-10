# -*- coding: utf-8 -*-
"""
Custom Dynamic Genre Driver
Allows runtime instantiation and registration of completely novel, bespoke,
or user-defined genres without modifying core driver code.
"""

from __future__ import annotations

from typing import Any
from .base_driver import BaseGenreDriver, register_genre


class CustomDynamicGenreDriver(BaseGenreDriver):
    """Dynamic genre driver supporting runtime configuration."""

    def __init__(
        self,
        genre_id: str,
        genre_name: str,
        description: str = "",
        power_levels: list[str] | None = None,
        currencies: list[str] | None = None,
        taboo_rules: list[str] | None = None,
        travel_speed_limits: dict[str, float] | None = None,
        banned_words: list[str] | None = None,
        institutional_translations: dict[str, str] | None = None,
    ):
        self.genre_id = genre_id.upper()
        self.genre_name = genre_name
        self.description = description
        self.power_levels = power_levels or []
        self.currencies = currencies or []
        self.taboo_rules = taboo_rules or []
        self.travel_speed_limits = travel_speed_limits or {
            "WALK": 60.0,
            "HORSE": 150.0,
            "CARRIAGE": 100.0,
            "CAR": 800.0,
            "TRAIN": 2000.0,
            "FLIGHT": 10000.0,
            "TELEPORT": 999999.0,
        }
        self.banned_words = banned_words or []
        self.institutional_translations = institutional_translations or {}

    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        c_no = chapter_payload.get("chapter_no", 0)
        full_text = str(chapter_payload)
        for err in self.check_immersion_lexicon(full_text):
            violations.append(f"Ch {c_no}: {err}")
        return violations


def create_custom_genre(
    genre_id: str,
    genre_name: str,
    description: str = "",
    power_levels: list[str] | None = None,
    currencies: list[str] | None = None,
    taboo_rules: list[str] | None = None,
    travel_speed_limits: dict[str, float] | None = None,
    banned_words: list[str] | None = None,
    institutional_translations: dict[str, str] | None = None,
) -> CustomDynamicGenreDriver:
    """Factory function to dynamically construct and register a new genre at runtime."""
    driver = CustomDynamicGenreDriver(
        genre_id=genre_id,
        genre_name=genre_name,
        description=description,
        power_levels=power_levels,
        currencies=currencies,
        taboo_rules=taboo_rules,
        travel_speed_limits=travel_speed_limits,
        banned_words=banned_words,
        institutional_translations=institutional_translations,
    )
    register_genre(driver)
    return driver
