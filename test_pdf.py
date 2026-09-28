from app.services.pdf_service import save_pdf


panels = []

for i in range(1, 6):
    panels.append(
        {
            "number": i,
            "image_url": f"/static/panels/panel_{i}.png",
            "scene": f"Comic panel {i}",
            "dialogue": "The adventure continues."
        }
    )


pdf_url = save_pdf(
    "ComicCraft AI Test",
    panels
)

print("PDF CREATED:")
print(pdf_url)