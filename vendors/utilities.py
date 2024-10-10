from datetime import datetime
import os
from flask import abort
from vendors.predictor import prepare_image
from werkzeug.utils import secure_filename
import uuid


ALLOWED_EXTENSIONS = {
    'png',
    'jpg',
    'jpeg'
}


UPLOAD_FOLDER = 'uploads'


def get_file():
    return

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        abort(400, 'Invalid file submitted.')

    if file and allowed_file(file.filename):

        filename = str(uuid.uuid4()) + secure_filename(file.filename)

        file_data = file.read()

        image_data, image = prepare_image(file_data)

    image.save(os.path.join(UPLOAD_FOLDER, filename))

    return UPLOAD_FOLDER + '/' + filename