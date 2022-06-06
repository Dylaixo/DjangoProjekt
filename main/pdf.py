import io
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def pdfbuffer(cart):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    p.setFont("Arial", 12)
    attractions_list = list(cart.attractions.all())
    height = 100 + 120 * len(attractions_list)
    p.setPageSize((600,height))
    p.drawString(250,800,"Plan")
    y = 150
    for attraction in attractions_list:
        img_tmp = Image.open(attraction.image)
        p.drawInlineImage(img_tmp,75,y-75,100,100)
        p.drawString(200, y, "Nazwa: " + attraction.name)
        p.drawString(200, y - 30, "Cena: " + str(attraction.price) + "zl")
        p.drawString(200, y - 60, "Szacowany czas: " + str(attraction.time))
        y = y + 120

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return buffer
