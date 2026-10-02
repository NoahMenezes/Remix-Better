"""Separation: audio file -> dict of stem arrays (Demucs htdemucs).

Lazy imports inside functions so this module imports without torch/demucs
installed. When deps are missing, functions raise a friendly RuntimeError
telling the user the exact pip command (torch install still running in bg).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # only for type checkers, never at runtime
    import numpy as np

STEMS = ("vocals", "drums", "bass", "other")
DEFAULT_MODEL = "htdemucs"
MODEL_SAMPLE_RATE = 44100


def _get_device() -> str:
    """Return 'cuda' if torch+CUDA is available, else 'cpu' (lazy import)."""
    try:
        import torch
    except ImportError:
        return "cpu"
    try:
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def _load_model(name: str = DEFAULT_MODEL, device: str | None = None) -> Any:
    """Load a Demucs pretrained model (htdemucs) onto device.

    Args:
        name: Demucs model name, e.g. "htdemucs".
        device: "cuda", "cpu", or None for auto-detect.

    Raises:
        RuntimeError: with install instructions if torch/demucs missing.
    """
    try:
        import torch
    except ImportError as e:
        raise RuntimeError(
            "torch is not installed yet (your background pip install is still "
            "running). Wait for it, then run: "
            "./venv/bin/pip install torch --index-url "
            "https://download.pytorch.org/whl/cu121"
        ) from e
    try:
        from demucs.pretrained import get_model
    except ImportError as e:
        raise RuntimeError(
            "demucs is not installed. Run: ./venv/bin/pip install -r requirements.txt"
        ) from e

    if device is None:
        device = _get_device()
    model = get_model(name)
    model.eval()
    # fp16 halves VRAM — matters on the 4GB RTX 3050 Mobile.
    if device == "cuda":
        try:
            model.half()
        except Exception:
            pass
    model.to(device)
    return model


def separate(
    audio_path: str,
    model_name: str = DEFAULT_MODEL,
    device: str | None = None,
) -> dict[str, np.ndarray]:
    """Split an audio file into 4 stems with Demucs htdemucs.

    Args:
        audio_path: Path to input audio file (mp3/wav).
        model_name: Demucs checkpoint name (default "htdemucs").
        device: "cuda"/"cpu"/None (auto). Auto falls back to CPU when no GPU.

    Returns:
        Dict keyed by "vocals"|"drums"|"bass"|"other", each an np.ndarray
        of shape (channels, samples) at the model's sample rate (44100 Hz).
    """
    import os

    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Input file not found: {audio_path}")

    try:
        import torch
    except ImportError as e:
        raise RuntimeError(
            "torch is not installed yet (background pip install still running). "
            "Wait for it to finish, then: ./venv/bin/pip install -r requirements.txt"
        ) from e
    try:
        import numpy as np
        import soundfile as sf
    except ImportError as e:
        raise RuntimeError(
            "numpy/soundfile missing. Run: ./venv/bin/pip install -r requirements.txt"
        ) from e
    try:
        from demucs.apply import apply_model
    except ImportError as e:
        raise RuntimeError(
            "demucs is not installed. Run: ./venv/bin/pip install -r requirements.txt"
        ) from e

    dev = device or _get_device()
    model = _load_model(model_name, dev)
    target_sr = int(getattr(model, "samplerate", MODEL_SAMPLE_RATE))

    # Load as (samples, channels) -> transpose to (channels, samples).
    data, sr = sf.read(audio_path, always_2d=True)
    wav = np.transpose(data, (1, 0)).astype("float32")
    if sr != target_sr:
        wav = _resample(wav, sr, target_sr)

    mix = torch.from_numpy(wav)
    ref = mix.dtype
    if dev == "cuda":
        mix = mix.half()
    mix = mix.to(dev)[None]  # (1, channels, samples)

    with torch.no_grad():
        # split+overlap keeps peak VRAM low enough for 4GB cards.
        out = apply_model(model, mix, shifts=1, split=True, overlap=0.25, progress=True)[0]
    out = out.to("cpu")
    if ref == torch.float32:
        out = out.float()
    stems_np = out.numpy()  # (n_sources, channels, samples)

    names: list[str] = [str(s) for s in getattr(model, "sources", ["drums", "bass", "other", "vocals"])]
    result: dict[str, np.ndarray] = {}
    for i, name in enumerate(names):
        key = name.lower()
        if key in STEMS:
            result[key] = np.ascontiguousarray(stems_np[i])
    missing = [s for s in STEMS if s not in result]
    if missing:
        raise RuntimeError(f"Demucs output missing stems {missing} (got {names})")
    return result


def _resample(wav_channels_first: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    """Resample (channels, samples) array; tries torchaudio, then librosa."""
    if sr_in == sr_out:
        return wav_channels_first
    try:
        import torch

        have_torch_audio = False
        try:
            import torchaudio.functional as taf

            have_torch_audio = True
        except ImportError:
            taf = None  # type: ignore
        if have_torch_audio:
            t = torch.from_numpy(wav_channels_first)
            return taf.resample(t, sr_in, sr_out).numpy().astype("float32")
    except Exception:
        pass
    try:
        import librosa

        outs = [librosa.resample(ch, orig_sr=sr_in, target_sr=sr_out) for ch in wav_channels_first]
        import numpy as np

        min_len = min(len(o) for o in outs)
        return np.stack([o[:min_len] for o in outs]).astype("float32")
    except ImportError as e:
        raise RuntimeError(
            f"Input is {sr_in} Hz but model needs {sr_out} Hz and no resampler "
            "(torchaudio/librosa) is installed."
        ) from e
