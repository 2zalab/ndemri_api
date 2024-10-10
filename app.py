from flask import Flask, flash, request, redirect, send_from_directory

from vendors.auth import check_pin_against_phone, check_phone
from vendors.cache import get_soil_records
from vendors.predictor import make_predictions
from vendors.quries import store_prediction_record, init_db, create_db
from vendors.utilities import save_file

app = Flask(__name__)


@app.route('/login')
def login():

    pin = request.form.get('pin')
    phone = request.form.get('phone')

    if None not in (pin, phone):
        return check_pin_against_phone(app, pin, phone)

    elif None not in phone:
        return check_phone(app, phone)

    return None

@app.route('/predictions/<id>')
def predictions(id):
    return get_soil_records(id)

@app.route('/predict', methods=['POST'])
def predict():

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    file_path = save_file(file)

    prediction = make_predictions(file_path)

    store_prediction_record(app, request.form.get('id'), file_path, prediction, request.form)

    return prediction

@app.route('/uploads/<path:path>')
def send_report(path):
    print(path)
    return send_from_directory('uploads', path)

@app.route('/')
def index():
    return '''
        <!doctype html>
        <title>Upload Soil Image</title>
        <h1>Upload Soil Image</h1>
        <form action="/predict" method=post enctype=multipart/form-data>
          <input type=int name=id placeholder=id>
          <input type=text name=name placeholder=name>
          <input type=text name=longitude placeholder=longitude>
          <input type=text name=latitude placeholder=latitude>
          <input type=file name=file required>
          <input type=submit value=Upload>
        </form>
        '''

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db(app)
    create_db(app)
    print('Initialized the database.')

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=5000)