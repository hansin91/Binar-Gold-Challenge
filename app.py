import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, flash, redirect, jsonify, request
from flasgger import LazyJSONEncoder, LazyString, Swagger, swag_from
from werkzeug.utils import secure_filename
from cleansing import cleanse_text
from report import getMostCommonWordsInNegativeTweet, getMostCommonWordsInPositiveTweet, getMostCommonWordsInTweet, generatePieChart, generateGroupHateSpeeh, generateIndividualHateSpeeh, generateClassificationHateSpeechBarChart, generateCharacteristicHateSpeechBarChart, generateSentimentChart, generateNegativeTweetChart

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bootstrap = Bootstrap4(app)

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
    sentimentChart = generateSentimentChart()
    negativeChart = generateNegativeTweetChart()
    null, characteristicHateSpeechDf  = generateCharacteristicHateSpeechBarChart()
    typeOfHateSpeechPieChart = generatePieChart(characteristicHateSpeechDf, 'Karakter Hate Speech')
    null, classificationcHateSpeechDf  = generateClassificationHateSpeechBarChart()
    classificationHateSpeechPieChart = generatePieChart(classificationcHateSpeechDf, 'Klasifikasi Hate Speech')
    individualHateSpeechBarChart, individualHateSpeechDf  = generateIndividualHateSpeeh()
    groupHateSpeechBarChart, groupHateSpeechDf = generateGroupHateSpeeh()
    negativeWords = getMostCommonWordsInNegativeTweet()
    positiveWords = getMostCommonWordsInPositiveTweet()
    return render_template('index.html',
        zip=zip,
        negativeWordsColums = negativeWords.columns.values,
        negativeWordsRowData = list(negativeWords.values.tolist()),
        positiveWordsColums = positiveWords.columns.values,
        positiveWordsRowData = list(positiveWords.values.tolist()),
        characteristicHateSpeechColumns = characteristicHateSpeechDf.columns.values,
        characteristicHateSpeechRowData = list(characteristicHateSpeechDf.values.tolist()),
        classificationcHateSpeechColumns = classificationcHateSpeechDf.columns.values, 
        classificationHateSpeechRowData = list(classificationcHateSpeechDf.values.tolist()),
        individualHateSpeechColumns = individualHateSpeechDf.columns.values,
        individualHateSpeechRowData = list(individualHateSpeechDf.values.tolist()),
        groupHateSpeechColumns = groupHateSpeechDf.columns.values,
        groupHateSpeechRowData = list(groupHateSpeechDf.values.tolist()),
        sentimentChart=sentimentChart,
        typeOfHateSpeechPieChart=typeOfHateSpeechPieChart,
        individualHateSpeechBarChart=individualHateSpeechBarChart,
        groupHateSpeechBarChart=groupHateSpeechBarChart,
        classificationHateSpeechPieChart=classificationHateSpeechPieChart,
        negativeChart=negativeChart)

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
        df = df.dropna()
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
    app.run(port=5000, debug=True)