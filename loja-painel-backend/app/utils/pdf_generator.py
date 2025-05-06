from app.models import Venda
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io


def gerar_pdf_venda(venda_id):
    venda = Venda.query.get(venda_id)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    pdf.setFont("Helvetica", 14)
    pdf.drawString(100, y, f"Nota de Venda #{venda.id}")
    y -= 30

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y, f"Cliente: {venda.cliente.nome}")
    y -= 20
    pdf.drawString(100, y, f"Data {venda.data.strftime('%d/%m/%Y %H:%M')}")
    y -= 40

    pdf.drawString(100, y, "Itens:")
    y -= 20

    for item in venda.itens:
        linha = f'{item.produto.nome} - {item.quantidade} x R${
            item.preco_unitario:2f}'
        pdf.drawString(120, y, linha)
        y -= 20

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y, f"Total: R${venda.total:.2f}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
