from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

app = Flask(__name__)

# Sample checklist items
checklist_items = [
    "Check engine oil level",
    "Inspect brake pads",
    "Check tire pressure",
    "Inspect headlights",
    "Check windshield wipers"
]

@app.route('/', methods=['GET', 'POST'])
def checklist():
    if request.method == 'POST':
        # Get checklist data from the form
        statuses = request.form.getlist('status')
        comments = request.form.getlist('comment')

        # Extract items identified as "Not Ok"
        not_ok_items = [item for item, status in zip(checklist_items, statuses) if status == 'Not Ok']

        # Generate PDF report
        pdf_data = generate_pdf_report(not_ok_items)

        # Return a response with PDF file as attachment
        return send_file(
            BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=True,
            attachment_filename='not_ok_items_report.pdf'
        )
    else:
        return render_template('checklist.html', items=checklist_items)

def generate_pdf_report(not_ok_items):
    # Check if there are any not-okay items
    if not not_ok_items:
        return "No items identified as Not Ok."

    # Create a PDF report
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []

    # Add title
    elements.append(Table([["Items Identified as Not Ok"]], style=[('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'), ('SIZE', (0, 0), (-1, -1), 16)]))
    elements.append(Table([[item] for item in not_ok_items], style=[('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('SIZE', (0, 0), (-1, -1), 12)]))

    # Build PDF
    doc.build(elements)
    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_data

if __name__ == '__main__':
    app.run(debug=True)
