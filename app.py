import sqlite3
import os
import pandas as pd

from flask import Flask, flash, redirect, url_for, jsonify, request
from flasgger import LazyJSONEncoder, LazyString, Swagger, swag_from
from werkzeug.utils import secure_filename
from cleansing import cleanse_text

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
      'title':  LazyString(lambda: 'Text and Data Cleansing API'),
      'version':  LazyString(lambda: '1.0.0'),
      'description': LazyString(lambda: 'API Documentation for cleansing text and data')
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

#database connection
conn = sqlite3.connect('db/text_processing.db', check_same_thread=False)
c = conn.cursor()
print('Opened database successfully')

c.execute('''CREATE TABLE IF NOT EXISTS data (original_text text, cleaned_text text);''')
print('Table created successfully')

@app.route('/', methods=['GET'])
def homepage():
    a =  [1,2,4]
    b = ['Ronaldo', 'Mbappe', 'Benzema']
    data = zip(a, b)
    json_response = {
        'status_code': 200,
        'description': 'Text Cleansing',
        'data': tuple(data)
    }
    response_data = jsonify(json_response)
    return response_data

@swag_from('docs/text_cleansing.yml', methods=['POST'])
@app.route('/text-cleansing', methods=['POST'])
def text_cleansing():
    text = request.form.get('text')
    cleaned_text = cleanse_text(text)
    json_response = {
        'status_code': 200,
        'description': 'Text Cleansing',
        'original_text': text,
        'cleaned_text': cleaned_text
    }
    response_data = jsonify(json_response)
    c.execute("INSERT INTO data (original_text, cleaned_text) values(?,?)",(text, cleaned_text)) 
    conn.commit()
    c.close()
    conn.close()
    return response_data

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   

@swag_from('docs/file_uploading.yml', methods=['POST'])
@app.route('/file-uploading', methods=['POST'])
def file_uploading():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        url_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(url_path)
        df = pd.read_csv(url_path, encoding='latin-1')
        df = df.iloc[:, 0]
        text_array = []
        c.execute('BEGIN TRANSACTION')
        for text in df:
            cleaned_text = cleanse_text(text)
            obj_text = {
                'cleaned_text': cleaned_text,
                'original_text': text
            }
            text_array.append(obj_text)
            c.execute("INSERT OR IGNORE INTO data (original_text, cleaned_text) values(?,?)",(text, cleaned_text)) 
        c.execute('COMMIT')
        json_response = {
            'status_code': 200,
            'description': 'Text Cleansing',
            'data': text_array
        }
        response_data = jsonify(json_response)
        return response_data

if __name__ == '__main__':
    app.run(port=5000)