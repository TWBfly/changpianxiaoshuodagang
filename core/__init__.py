# -*- coding: utf-8 -*-
"""
Core Narrative Engine Package
Contains:
- dynamic_fingerprints: 8-mode chapter structure fingerprints
- narrative_physics: Spatiotemporal continuity, item chain of custody, real counterforces
- scalable_blueprint: Scalable multi-volume, 200/300/400+ chapters macro-generator
"""

from .dynamic_fingerprints import FINGERPRINT_SPECS, validate_chapter_fingerprint
from .narrative_physics import NarrativePhysicsValidator
from .scalable_blueprint import UniversalScalableBlueprint

__all__ = [
    "FINGERPRINT_SPECS",
    "validate_chapter_fingerprint",
    "NarrativePhysicsValidator",
    "UniversalScalableBlueprint",
]
