from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client['PesoIdeal']
imc_collection = db['imc_data']

@app.route('/api/calculate-imc', methods=['POST'])
def calculate_imc():
    data = request.json
    weight = float(data['weight'])
    height = float(data['height'])

    imc = weight / (height ** 2)
    imc_rounded = round(imc, 2)

    if imc < 18.5:
        classification = 'Abaixo do peso'
    elif imc < 24.9:
        classification = 'Peso normal'
    elif imc < 29.9:
        classification = 'Sobrepeso'
    elif imc < 34.9:
        classification = 'Obesidade grau 1'
    elif imc < 39.9:
        classification = 'Obesidade grau 2'
    else:
        classification = 'Obesidade grau 3'

    imc_data = {
        'weight': weight,
        'height': height,
        'imc': imc_rounded,
        'classification': classification
    }
    imc_collection.insert_one(imc_data)

    return jsonify({
        'imc': imc_rounded,
        'classification': classification
    })

if __name__ == '__main__':
    app.run(debug=True)
