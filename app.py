"""Gradio entry point (Phase 7). Scaffold only — no pipeline logic yet."""
from __future__ import annotations


def build_demo():
    """Build the Gradio Blocks UI. Gradio is imported lazily so this file
    imports even when gradio is not installed (pre-Phase 0)."""
    try:
        import gradio as gr
    except ImportError as e:
        raise RuntimeError(
            "gradio is not installed. Run: ./venv/bin/pip install -r requirements.txt"
        ) from e

    with gr.Blocks(title="Remix-Better") as demo:
        gr.Markdown("# Remix-Better\nUpload a song, pick a stem, describe the replacement.")
        audio_in = gr.Audio(type="filepath", label="Upload song")
        stem = gr.Radio(["vocals", "drums", "bass", "other"], label="Stem to replace")
        prompt = gr.Textbox(label="Replacement description")
        out = gr.Audio(label="Remixed result")
        btn = gr.Button("Generate")
        btn.click(fn=lambda *a: (_ for _ in ()).throw(RuntimeError("Phase 7: not wired yet")),
                  inputs=[audio_in, stem, prompt], outputs=out)
    return demo


if __name__ == "__main__":
    build_demo().launch()
