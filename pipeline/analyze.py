"""Analysis: kept stems -> {bpm, key} via librosa.

Phase 2 stub only. Lazy imports so this imports without librosa installed.
"""
from __future__ import annotations


def analyze(stem_paths: list[str]) -> dict:
    """Estimate tempo and key from kept stems.

    Args:
        stem_paths: List of audio file paths to analyze.

    Returns:
        {"bpm": float, "key": str} e.g. {"bpm": 120.0, "key": "A minor"}.
    """
    raise NotImplementedError("Phase 2: BPM/key analysis not implemented yet")
