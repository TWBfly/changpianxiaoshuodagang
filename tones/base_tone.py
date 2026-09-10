# -*- coding: utf-8 -*-
"""
Universal Tone Driver Base Interface & Registry
Defines the contract for emotional tone, catharsis rhythm, tension-release curves,
dialogue ethos, and tone-specific narrative constraints across web novel genres.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseToneDriver(ABC):
    """Abstract base class for emotional tone and dramatic ethos drivers."""

    tone_id: str = "BASE_TONE"
    tone_name: str = "Base Emotional Tone"
    description: str = ""

    # Tension curve archetype:
    # 'FAST_CATHARSIS' (爽文), 'COMIC_INVERSION' (搞笑), 'HIGH_TENSION_NOIR' (悬疑严肃),
    # 'TRAGIC_EROSION' (虐文), 'SACRIFICIAL_HYMN' (悲壮), 'PASSIONATE_ROAR' (热血)
    tension_curve: str = "FAST_CATHARSIS"

    # Maximum consecutive suppression/humiliation beats allowed without counter-foreshadowing
    max_oppression_beats: int = 3

    # Key emotional payoff indicators expected in chapters
    required_emotional_payoffs: list[str] = []

    # Forbidden tropes that destroy this specific tone
    forbidden_tone_tropes: list[str] = []

    # Suggested rhetorical and dialogue flavors
    dialogue_flavor: list[str] = []

    @abstractmethod
    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        """
        Validate whether a chapter's dramatic beats and emotional direction
        align with this tone. Returns a list of violation error strings.
        """
        pass

    def check_forbidden_tropes(self, text: str) -> list[str]:
        """Check if chapter text contains forbidden emotional/rhetorical tropes."""
        violations = []
        for trope in self.forbidden_tone_tropes:
            if trope in text:
                violations.append(f"Tone violation in [{self.tone_name}]: forbidden trope '{trope}' found")
        return violations


# --- Global Tone Registry ---
_TONE_REGISTRY: dict[str, BaseToneDriver] = {}


def register_tone(driver: BaseToneDriver) -> None:
    """Register an emotional tone driver instance."""
    _TONE_REGISTRY[driver.tone_id.upper()] = driver


def get_tone_driver(tone_id: str) -> BaseToneDriver:
    """Retrieve an emotional tone driver by ID, case-insensitive."""
    key = tone_id.strip().upper()
    if key not in _TONE_REGISTRY:
        raise KeyError(f"Unknown tone_id '{tone_id}'. Registered: {list(_TONE_REGISTRY.keys())}")
    return _TONE_REGISTRY[key]


def list_registered_tones() -> list[str]:
    """Return all registered tone IDs."""
    return list(_TONE_REGISTRY.keys())


class CustomDynamicToneDriver(BaseToneDriver):
    """Dynamic custom tone driver created at runtime."""

    def __init__(
        self,
        tone_id: str,
        tone_name: str,
        description: str = "",
        tension_curve: str = "FAST_CATHARSIS",
        max_oppression_beats: int = 3,
        required_emotional_payoffs: list[str] | None = None,
        forbidden_tone_tropes: list[str] | None = None,
    ):
        self.tone_id = tone_id.upper()
        self.tone_name = tone_name
        self.description = description
        self.tension_curve = tension_curve
        self.max_oppression_beats = max_oppression_beats
        self.required_emotional_payoffs = required_emotional_payoffs or []
        self.forbidden_tone_tropes = forbidden_tone_tropes or []

    def validate_chapter_tone(self, chapter_payload: dict[str, Any]) -> list[str]:
        violations = []
        full_text = str(chapter_payload)
        violations.extend(self.check_forbidden_tropes(full_text))
        return violations


def create_custom_tone(
    tone_id: str,
    tone_name: str,
    description: str = "",
    tension_curve: str = "FAST_CATHARSIS",
    max_oppression_beats: int = 3,
    required_emotional_payoffs: list[str] | None = None,
    forbidden_tone_tropes: list[str] | None = None,
) -> CustomDynamicToneDriver:
    """Factory function to dynamically construct and register a custom tone."""
    driver = CustomDynamicToneDriver(
        tone_id=tone_id,
        tone_name=tone_name,
        description=description,
        tension_curve=tension_curve,
        max_oppression_beats=max_oppression_beats,
        required_emotional_payoffs=required_emotional_payoffs,
        forbidden_tone_tropes=forbidden_tone_tropes,
    )
    register_tone(driver)
    return driver
