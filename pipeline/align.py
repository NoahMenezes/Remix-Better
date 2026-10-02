"""Alignment: time-stretch + trim/pad generated clip to match target.

Phase 4 stub only. Lazy imports so this imports without pyrubberband installed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


def align(
    audio: np.ndarray, source_bpm: float, target_bpm: float, target_length: float
) -> np.ndarray:
    """Stretch/trim generated audio to match target tempo and length.

    Args:
        audio: Generated audio array.
        source_bpm: Tempo of the generated audio.
        target_bpm: Tempo of the original track.
        target_length: Exact target length in seconds.

    Returns:
        Aligned audio array.
    """
    raise NotImplementedError("Phase 4: alignment not implemented yet")
