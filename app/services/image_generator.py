from pathlib import Path

import torch
from diffusers import DiffusionPipeline

from app.config import PANELS_DIR


MODEL_ID = "segmind/tiny-sd"

_pipeline = None


def get_pipeline():
    global _pipeline

    if _pipeline is None:
        print("Loading local AI image model...")

        _pipeline = DiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float32
        )

        _pipeline = _pipeline.to("cpu")

        print("Local AI image model loaded.")

    return _pipeline


def generate_panel_image(panel, filename):
    pipeline = get_pipeline()

    scene = panel.get("scene", "")
    dialogue = panel.get("dialogue", "")

    prompt = f"""
    Colorful cartoon comic-book illustration.
    A clean friendly college project comic panel.
    Scene: {scene}
    Characters and action: {dialogue}
    Bright colorful cartoon style.
    Landscape composition.
    Clear simple background.
    No text, no speech bubbles, no captions.
    """

    print(f"Generating AI image for panel {panel.get('number', '')}...")

    result = pipeline(
        prompt,
        num_inference_steps=50,
        guidance_scale=7.5
    )

    image = result.images[0]

    path = PANELS_DIR / filename
    image.save(path, format="PNG")

    print(f"AI panel saved: {path}")

    return f"/static/panels/{filename}"