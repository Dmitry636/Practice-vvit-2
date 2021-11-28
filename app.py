import os
import requests
import uuid
import json
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template,request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    # Чтение данных из формы
    original_text = request.form['text']
    target_language = request.form['language']

    # Загрузка данных из .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Указываем что хотим перевести в API
    # Версия (3.0) и цельевой язык
    path = '/translate?api-version=3.0'

    # Добавление цельевого параметра языка
    target_language_parameter = '&to=' + target_language

    # Создание полного URL 
    constructed_url = endpoint + path + target_language_parameter

    # Настройка информации заголовка, которая включает мой ключ
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Создание тела запроса с текстом, который будет переведен
    body = [{'text': original_text}]

    # Делаем вызов используя post
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)

    # Извлечение JSON отклика
    translator_response = translator_request.json()

    translated_text = translator_response[0]['translations'][0]['text']

    # Вызов рендера шаблонов, передача переведенного текста, исходного текста и указываемого языка в шаблон
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )