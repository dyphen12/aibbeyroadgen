"""
application.py

This module contains the API for the Aibbey Road project.

"""

from flask import Flask, request
from werkzeug.utils import secure_filename
import random
from flask import send_file

from aibbeyroad import core, abutils

app = Flask(__name__)

UPLOAD_FOLDER = '/' + abutils.load_config().seeds_folder

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def hello_world():
    """
    This function is the default route for the API.
    :return: string

    Notes: Deprecating this function
    """
    return "Hello World"

@app.route("/upload-midi", methods=['POST','PUT'])
def process_midi():
    """
    This function processes the midi file and returns the generated midi file.
    :return: file
    """

    file = request.files['file']
    filename=secure_filename(file.filename)

    preprocessname = 'preprocess-' + str(random.randint(1000, 9999)) + '-' + secure_filename(file.filename)

    filedir = abutils.load_config().seeds_folder + '/' + preprocessname

    file.save(filedir)

    #print(filename)

    core.generate_midi_for_web(filedir,4)

    gname = filedir.replace('preprocess', 'generated')
    gname = gname.replace(abutils.load_config().seeds_folder, 'generated')

    return send_file(gname)



@app.route("/upload-midi-s3", methods=['POST','PUT'])
def process_midi_s3():
    """
    This function processes the midi file and uploads the generated file to an AWS S3 bucket.
    :return: string
    """

    file = request.files['file']
    filename=secure_filename(file.filename)

    preprocessname = 'preprocess-' + str(random.randint(10000, 99999)) + '-' + secure_filename(file.filename)

    filedir = abutils.load_config().seeds_folder + '/' + preprocessname

    file.save(filedir)

    #print(filename)

    core.generate_midi_for_aws(filedir,4,abutils.load_config().seeds_folder)

    gname = filedir.replace('preprocess', 'generated')
    gname = gname = gname.replace(abutils.load_config().seeds_folder, 'generated')
    gbucketname = preprocessname.replace('preprocess', 'generated')

    print('Generated MIDI: ' + gname.replace('generated/', abutils.load_config().bucket + '/' + abutils.load_config().folder + "/"))

    response = abutils.upload_file(gname, gbucketname)

    if response:
        #print('Uploaded to S3')
        return 'Uploaded to S3'
    else:
        #print('Upload failed')
        return 'Upload failed'




if __name__ == "__main__":
    app.run()