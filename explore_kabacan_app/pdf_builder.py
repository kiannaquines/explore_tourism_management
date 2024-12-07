import io
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from datetime import datetime

def pdf_builder(
    chart_buffers,
    pdf_title="Tourist Report",
    subtitle="Explore Kabacan Management System",
    output_filename="tourist_report.pdf",
):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{output_filename}"'
    today = datetime.today()

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=10,
        bottomMargin=72,
        pagesize=letter,
    )

    doc.title = "Statiscal Document for Explore Kabacan"
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    header_style = ParagraphStyle(
        "Header",
        parent=styles["Heading1"],
        fontSize=13,
        spaceAfter=0,
        alignment=1,
        textColor=colors.black,
    )

    title = Paragraph(f"{subtitle}", header_style)
    third_title = Paragraph(
        f"Date Generated: {today.strftime('%Y-%m-%d')}", header_style
    )
    second_title = Paragraph(f"{pdf_title}", header_style)
    elements.append(title)
    elements.append(third_title)
    elements.append(second_title)

    elements.append(Paragraph("<br />", normal_style))

    for chart_buf in chart_buffers:
        chart_image = ImageReader(chart_buf)
        chart_width, chart_height = chart_image.getSize()
        aspect_ratio = chart_height / chart_width
        new_width = 440
        new_height = new_width * aspect_ratio
        chart = Image(chart_buf, width=new_width, height=new_height)
        elements.append(chart)
        elements.append(Paragraph("<br />", normal_style))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response