# -*- coding: utf-8 -*-
"""
Universal Genre Driver Base Interface & Registry
Defines the contract for genre-adaptive narrative physics, power levels,
currencies, taboo rules, and institutional translations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseGenreDriver(ABC):
    """Abstract base class for genre-specific narrative drivers."""

    genre_id: str = "BASE"
    genre_name: str = "Base Genre"
    description: str = ""

    # Power progression ladder
    power_levels: list[str] = []

    # Economic and resource mediums
    currencies: list[str] = []

    # Inviolable physical / worldview taboo rules (violation = fatal logic bug)
    taboo_rules: list[str] = []

    # Max speed of travel (li/day or custom metric per mode)
    # Default units: 里 (Chinese li, ~500m) per story day
    travel_speed_limits: dict[str, float] = {
        "WALK": 60.0,
        "HORSE": 150.0,
        "CARRIAGE": 100.0,
        "FLEET_WATER": 200.0,
        "MARCH_ARMY": 80.0,
        "FLY_SWORD": 2000.0,
        "TELEPORT": 999999.0,
    }

    # Banned words breaking immersion in this genre
    banned_words: list[str] = []

    # Translations for modern concepts into native in-world institutions
    institutional_translations: dict[str, str] = {}

    def translate_term(self, term: str) -> str:
        """Translate a concept into native genre vocabulary."""
        return self.institutional_translations.get(term, term)

    @abstractmethod
    def validate_chapter_mechanics(self, chapter_payload: dict[str, Any]) -> list[str]:
        """
        Validate whether a chapter's beats, costs, and stakes comply with
        this genre's worldview physics. Returns a list of error strings.
        """
        pass

    def check_immersion_lexicon(self, text: str) -> list[str]:
        """Check if text contains immersion-breaking words for this genre."""
        violations = []
        for word in self.banned_words:
            if word in text:
                violations.append(f"Immersion violation in {self.genre_name}: banned word '{word}' found")
        return violations


# --- Global Registry ---
_GENRE_REGISTRY: dict[str, BaseGenreDriver] = {}

_GENRE_ALIASES: dict[str, str] = {
    # Urban aliases
    "DUSHI": "URBAN_REALISTIC",
    "URBAN": "URBAN_REALISTIC",
    "DUSHI_XIUXIAN": "URBAN_SUPERNATURAL",
    "DUSHI_YINENG": "URBAN_SUPERNATURAL",
    "URBAN_CULTIVATION": "URBAN_SUPERNATURAL",
    # History aliases
    "JIAKONG": "HISTORICAL_ANCIENT",
    "HISTORY": "HISTORICAL_ANCIENT",
    "HISTORICAL": "HISTORICAL_ANCIENT",
    # Suspense aliases
    "XUANYI": "SUSPENSE_DETECTIVE",
    "SUSPENSE": "SUSPENSE_DETECTIVE",
    "DETECTIVE": "SUSPENSE_DETECTIVE",
    # Brain hole aliases
    "NAODONG": "BRAIN_HOLE",
    "HIGH_CONCEPT": "BRAIN_HOLE",
    # Republic aliases
    "MINGUO": "REPUBLIC_ERA",
    "ESPIONAGE": "REPUBLIC_ERA",
    # Cthulhu aliases
    "KESULU": "CTHULHU_WESTERN",
    "CTHULHU": "CTHULHU_WESTERN",
    "ELDRITCH": "CTHULHU_WESTERN",
    # Sci-Fi aliases
    "KEHUAN": "SCI_FI_CYBER",
    "SCIFI": "SCI_FI_CYBER",
    "CYBERPUNK": "SCI_FI_CYBER",
    # Game system aliases
    "YOUXI": "GAME_SYSTEM",
    "GAME": "GAME_SYSTEM",
    "SYSTEM": "GAME_SYSTEM",
    # Legacy & common aliases
    "XIANXIA": "XIANXIA",
    "XUANHUAN": "XIANXIA",
    "HORROR": "HORROR",
    "GUIYI": "HORROR",
    "INFINITE": "INFINITE_FLOW",
    "WUXIAN": "INFINITE_FLOW",
    "HONGHUANG": "HONGHUANG",
    "PREHISTORIC": "HONGHUANG",
}


def register_genre(driver: BaseGenreDriver) -> None:
    """Register a genre driver instance."""
    _GENRE_REGISTRY[driver.genre_id.upper()] = driver


def get_genre_driver(genre_id: str) -> BaseGenreDriver:
    """Retrieve a genre driver by ID, case-insensitive, supporting aliases."""
    key = genre_id.strip().upper()
    resolved_key = _GENRE_ALIASES.get(key, key)
    if resolved_key in _GENRE_REGISTRY:
        return _GENRE_REGISTRY[resolved_key]
    if key in _GENRE_REGISTRY:
        return _GENRE_REGISTRY[key]
    raise KeyError(f"Unknown genre_id '{genre_id}'. Registered: {list(_GENRE_REGISTRY.keys())}")


def list_registered_genres() -> list[str]:
    """Return all registered genre IDs."""
    return list(_GENRE_REGISTRY.keys())
