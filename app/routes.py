from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import ComicRequest
from app.services.gemini_service import generate_story
from app.services.image_generator import generate_panel_image
from app.services.pdf_service import save_pdf


router = APIRouter()

templates = Jinja2Templates(directory="templates")


def make_request(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    return ComicRequest(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style
    )


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,

    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    try:
        data = make_request(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style
        )

        panels = generate_story(data)

        final_panels = []

        for panel in panels:
            filename = f"panel_{panel['number']}.png"

            image_url = generate_panel_image(
                panel,
                filename
            )

            panel["image_url"] = image_url
            final_panels.append(panel)

        title = f"{character_name}'s Comic Adventure"

        pdf_url = save_pdf(
            title,
            final_panels
        )

        return templates.TemplateResponse(
            request=request,
            name="comic.html",
            context={
                "title": title,
                "panels": final_panels,
                "pdf_url": pdf_url
            }
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": str(exc)
            },
            status_code=500
        )