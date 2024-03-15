from flask import Flask, render_template, request

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
        checked_items = request.form.getlist('item')
        comments = request.form.getlist('comment')

        # Generate report
        report = []
        for item, comment in zip(checked_items, comments):
            report.append({'item': item, 'comment': comment})

        return render_template('report.html', report=report)
    else:
        return render_template('checklist.html', items=checklist_items)

if __name__ == '__main__':
    app.run(debug=True)
