"""Mix: kept stems + new aligned stem -> final mixed track.

Phase 5 stub only. Lazy imports so this imports without numpy/soundfile installed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


def mix(stems: dict[str, np.ndarray], output_path: str) -> str:
    """Combine stems into one mixed track.

    Args:
        stems: Dict of stem name -> audio array.
        output_path: Where to write the final mix.

    Returns:
        The output_path on success.
    """
    raise NotImplementedError("Phase 5: mixing not implemented yet")
