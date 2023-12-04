from flask import Flask

app = Flask(__name__)



def run(address:str, config:dict):
    ip, port = address.split(":")
    app.run(host="127.0.0.1", port=port)