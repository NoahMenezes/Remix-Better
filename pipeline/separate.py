"""Separation: audio file -> dict of stem arrays (Demucs htdemucs).

Phase 1 stub only — full implementation comes in Phase 1 commits.
Lazy imports inside the function so this module imports without torch/demucs installed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # only for type checkers, never at runtime
    import numpy as np

STEMS = ("vocals", "drums", "bass", "other")


def separate(audio_path: str) -> dict[str, np.ndarray]:
    """Split an audio file into 4 stems.

    Args:
        audio_path: Path to input audio file (mp3/wav).

    Returns:
        Dict keyed by stem name ("vocals", "drums", "bass", "other"),
        each value an np.ndarray of shape (channels, samples) or (samples, channels).
    """
    raise NotImplementedError("Phase 1: Demucs separation not implemented yet")
