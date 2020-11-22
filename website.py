from flask import Flask, request, render_template, send_file
import tempfile
import os
import uuid
from main import kal_datei_erstellen
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        c = kal_datei_erstellen(request.form.get("course"))
        f = tempfile.NamedTemporaryFile("w")
        f.writelines(c)
        return send_file(open(f.name, "rb"), "text/calendar", as_attachment=True, attachment_filename="Calendar.ics")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
