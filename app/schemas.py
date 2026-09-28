from pydantic import BaseModel


class ComicRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str


class ComicPanel(BaseModel):
    number: int
    scene: str
    dialogue: str
    narration: str
    image_prompt: str
    image_url: str