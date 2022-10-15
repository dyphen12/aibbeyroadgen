from flask import Flask, request
from werkzeug.utils import secure_filename
import random
from flask import send_file

from aibbeyroad import core

app = Flask(__name__)

UPLOAD_FOLDER = '/seeds'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#curl -X POST -F file=@"TearsInHeaven.mid" http://localhost:5000/upload-midi

#curl -X POST -F file=@"TearsInHeaven.mid" http://localhost:5000/upload-midi --output TearsInHeaven-generated.mid

@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/upload-midi", methods=['POST','PUT'])
def print_filename():
    file = request.files['file']
    filename=secure_filename(file.filename)

    preprocessname = 'preprocess-' + str(random.randint(1000, 9999)) + '-' + secure_filename(file.filename)

    filedir = 'seeds/' + preprocessname

    file.save(filedir)

    print(filename)

    core.generate_midi_for_web(filedir,4)

    gname = filedir.replace('preprocess', 'generated')
    gname = gname.replace('seeds', 'generated')

    return send_file(gname)

if __name__ == "__main__":
    app.run()