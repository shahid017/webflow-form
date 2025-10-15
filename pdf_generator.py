from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(form_data, output_filename="output.pdf"):
    try:
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=36, leftMargin=36,
            topMargin=36, bottomMargin=36
        )
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title = Paragraph("<b>Prescription Order Form</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        # Prepare data for table
        data = [
            ["First Name", form_data.get("OR-Name", "N/A")],
            ["Last Name", form_data.get("OR-Last-name", "N/A")],
            ["Phone Number", form_data.get("OR-Phone-number", "N/A")],
            ["Medication(s)", form_data.get("OR-Medication", "N/A")],
            ["Notes", form_data.get("OR-note", "N/A")],
            ["Delivery Option", form_data.get("delivery_option", "N/A")],
            ["Address", form_data.get("address", "N/A")],
            ["Preferred Time Slot", form_data.get("time_slot", "N/A")],
        ]

        # Create table
        table = Table(data, colWidths=[2.5 * inch, 3.5 * inch])  # Adjusted widths
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.3 * inch))

        footer = Paragraph("Generated automatically from Webflow Order Form", styles['Normal'])
        elements.append(footer)

        doc.build(elements)
        print(f"✅ PDF generated successfully: {os.path.abspath(output_filename)}")
        return output_filename

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        raise
