from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

prompt = """
Create a colorful comic-book style illustration.
A young student inventor is standing in a futuristic laboratory
with a small friendly robot.
Clean cartoon style, bright colors, landscape composition.
Do not add text or speech bubbles.
"""

response = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    ),
)

saved = False

for part in response.parts:
    if part.inline_data:
        image = part.as_image()
        image.save("test_ai_panel.png")
        saved = True
        print("AI IMAGE GENERATED: test_ai_panel.png")

if not saved:
    print("No image was returned.")