"""Generation: prompt + bpm + key -> generated stem audio (MusicGen-small).

Phase 3 stub only. Lazy imports so this imports without audiocraft/torch installed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


def generate(prompt: str, bpm: float, key: str, duration: float) -> np.ndarray:
    """Generate a replacement stem.

    Args:
        prompt: Text description of the replacement stem.
        bpm: Target tempo in beats per minute.
        key: Target musical key, e.g. "A minor".
        duration: Target duration in seconds.

    Returns:
        Generated audio as np.ndarray.
    """
    raise NotImplementedError("Phase 3: MusicGen generation not implemented yet")
