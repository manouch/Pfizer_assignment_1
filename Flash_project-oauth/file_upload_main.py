import json
import os
from scripts.translateAPI import translate

from cassandra.cqlengine import connection
from flask import Flask, flash, request, redirect, render_template, Response, current_app, send_from_directory, \
    make_response, session
from werkzeug.utils import secure_filename

#from models.user import Files

#connection.setup(['internal-aa192f871e59a4ac7ad1d7d479922bb2-304939937.us-east-1.elb.amazonaws.com'], "cqlengine", protocol_version=3)

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# this function is adding file to DB
def add_file(file_name, status):
    file = Files.create(file_name=file_name, status=status)

    file.save()

def call_translate(source_file_path, source_lang, target_lang):
    translate_obj = translate()
    auth = translate_obj.generate_auth_token()
    status = translate_obj.tranlsate_files(auth, source_file_path, source_lang, target_lang)
    if status == 'finished':
        return "Translated"
    else:
        return "ERROR"

#this will download the files
@app.route('/Translated_files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    Translated_files= r"C:\Users\GAURAK02\PycharmProjects\batchOCR\Translated_files"
    # Returning file from appended path
    return send_from_directory(directory=Translated_files, filename=filename)


@app.route('/', methods=['POST', 'GET'])
@app.route('/QueryStringInfo')
def upload_file():

            return render_template('upload.html')



if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = True)