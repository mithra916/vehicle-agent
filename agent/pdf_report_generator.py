from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf_report(results, health_score, filename="output/VehicleTestReport.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Vehicle Test Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 110, f"Overall Health Score: {health_score}/100")

    y = height - 150
    for result in results:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"--- {result['test']} ---")
        y -= 20

        c.setFont("Helvetica", 11)
        c.drawString(70, y, f"Result: {result['result']}")
        y -= 15
        if result['priority']:
            c.drawString(70, y, f"Priority: {result['priority']}")
            y -= 15
        if result['reason']:
            c.drawString(70, y, f"Reason: {result['reason']}")
            y -= 15
        if result['suggestion']:
            c.drawString(70, y, f"Suggestion: {result['suggestion']}")
            y -= 15

        y -= 10
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    print(f"\n✅ PDF Report saved as: {filename}")
