from pathlib import Path

from fpdf import FPDF

from app.config import BASE_DIR


EXPORT_DIR = BASE_DIR / "static" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_pdf(title, panels):
    safe_title = "".join(
        c if c.isalnum() else "_"
        for c in title
    )

    filename = f"{safe_title}.pdf"
    output = EXPORT_DIR / filename

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in panels:

        pdf.add_page()

        # Title
        pdf.set_font("Arial", "B", 18)
        pdf.cell(
            0,
            12,
            title,
            ln=True,
            align="C"
        )

        # Image
        image_url = panel["image_url"]
        image_path = BASE_DIR / image_url.lstrip("/")

        if image_path.exists():
            pdf.image(
                str(image_path),
                x=15,
                y=30,
                w=180
            )

        # Panel information
        pdf.set_y(155)

        pdf.set_font("Arial", "B", 12)

        pdf.multi_cell(
            180,
            7,
            f"Panel {panel['number']}: {panel['scene']}"
        )

        pdf.ln(3)

        pdf.set_font("Arial", "", 11)

        pdf.multi_cell(
            180,
            7,
            f"Dialogue: {panel['dialogue']}"
        )

    pdf.output(str(output))

    return f"/static/exports/{filename}"