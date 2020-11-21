
from flask import Flask, request, render_template, send_file
from main import kal_datei_erstellen
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return send_file(kal_datei_erstellen(request.form.get("course")), "text/calendar", as_attachment=True, attachment_filename="Calendar.ics")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
