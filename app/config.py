from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


APP_NAME = os.getenv("APP_NAME", "ComicCraft AI")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_TEXT_MODEL = os.getenv(
    "GEMINI_TEXT_MODEL",
    "gemini-3.5-flash-lite"
)

PANEL_COUNT = int(
    os.getenv("PANEL_COUNT", "5")
)

PANELS_DIR = BASE_DIR / "static" / "panels"

PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)