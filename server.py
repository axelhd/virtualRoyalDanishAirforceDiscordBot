from flask import Flask, request
import json
import os

app = Flask(__name__)


@app.route('/<string:data>')
def index(data):
    print(data)
    if data == 'poweroff':
        os.system('shutdown /s /t 0')

    return data


app.run(host="10.0.0.9")
