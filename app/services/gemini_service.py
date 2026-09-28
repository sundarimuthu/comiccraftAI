import json
import re

from app.config import (
    GEMINI_API_KEY,
    GEMINI_TEXT_MODEL,
    PANEL_COUNT
)


def clean_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```$",
            "",
            text
        )

    return text.strip()


def fallback_story(data):
    panels = []

    scenes = [
        "The main character begins an exciting journey.",
        "A mysterious discovery changes the situation.",
        "The character faces a difficult challenge.",
        "The character finds a clever solution.",
        "The adventure ends with a hopeful new beginning."
    ]

    for i in range(PANEL_COUNT):
        scene = scenes[i % len(scenes)]

        panels.append(
            {
                "number": i + 1,
                "scene": scene,
                "dialogue": (
                    f"{data.character_name}: "
                    f"This is an amazing adventure!"
                ),
                "narration": scene,
                "image_prompt": (
                    f"{data.character_name} in {data.setting}, "
                    f"{data.art_style} comic illustration, "
                    f"{data.tone} mood"
                )
            }
        )

    return panels


def generate_story(data):
    if not GEMINI_API_KEY:
        return fallback_story(data)

    try:
        from google import genai

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        prompt = f"""
Create a short comic story.

Story idea:
{data.story_prompt}

Main character:
{data.character_name}

Setting:
{data.setting}

Tone:
{data.tone}

Art style:
{data.art_style}

Create exactly {PANEL_COUNT} comic panels.

Return ONLY valid JSON.

Format:

[
  {{
    "number": 1,
    "scene": "scene description",
    "dialogue": "short dialogue",
    "narration": "short narration",
    "image_prompt": "visual description for the panel"
  }}
]

Do not use markdown.
Do not use code fences.
"""

        response = client.models.generate_content(
            model=GEMINI_TEXT_MODEL,
            contents=prompt
        )

        raw = clean_json(
            response.text
        )

        panels = json.loads(raw)

        if not isinstance(panels, list):
            raise ValueError(
                "Gemini returned invalid story format."
            )

        return panels[:PANEL_COUNT]

    except Exception as exc:
        print(
            "Gemini story generation failed:",
            exc
        )

        print(
            "Using local fallback story."
        )

        return fallback_story(data)