from flask import Flask, request, jsonify
from flask import send_from_directory
import requests as req
import json
import service
import const
import log

app = Flask(__name__)
app.register_blueprint(service.bp)


g_config = {}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


# 특정 노트 하나를 읽어옴
@app.route("/note/<int:note_id>", methods=['GET'])
def get_one_note(note_id):
    res = {}
    log.logging_client("REQUEST", request.method, request.path)
    note = service.load_note(note_id)
    if note == None:
        res = {"res" : const.FAIL, "msg" : "cannot found this note"}
    
    else:
        res = {"res" : const.OK, "note" : note} 
          
    log.logging_client("REPLY", request.method, request.path, res)
    return res


# 모든 노트를 읽어옴
@app.route("/note", methods=['GET'])
def get_all_note():
    log.logging_client("REQUEST", request.method, request.path)
    res = {"res" : const.OK, "data" : service.load_all_note()}
    log.logging_client("REPLY", request.method, request.path, res)
    return res



# 노트를 추가함 ID는 유니크한 값 - primary에서 제공
@app.route("/note", methods=['POST'])
def create_note():
    body =  request.get_json()
    log.logging_client("REQUEST", request.method, request.path, body)
    res = service.write_post(body)
    log.logging_client("REPLY", request.method, request.path, res)
    return res
    

# 노트를 덮어씀
@app.route("/note/<int:note_id>", methods=['PUT'])
def overwrite_note(note_id):
    body = request.get_json()
    log.logging_client("REQUEST", request.method, request.path, body)
    res = service.write_put(body, note_id)
    log.logging_client("REPLY", request.method, request.path, res)
    return res

# 노트를 수정함
@app.route("/note/<int:note_id>", methods=['PATCH'])
def modify_note(note_id):
    body = request.get_json()
    log.logging_client("REQUEST", request.method, request.path, body)
    res = service.write_patch(body, note_id)
    log.logging_client("REPLY", request.method, request.path, res)
    return res


# 노트를 삭제함 
@app.route("/note/<int:note_id>", methods=['DELETE'])
def delete_note(note_id):
    log.logging_client("REQUEST", request.method, request.path)
    res = service.write_delete(note_id)
    log.logging_client("REPLY", request.method, request.path, res)
    return res


# page not found 
@app.errorhandler(404)
def page_not_found(error):
    return send_from_directory("public", '404.html')


def run(re:str, config:dict, primary:str):
    global g_config 
    
    service.set_config(config)
    service.set_primary(primary)
    service.set_service_address(re)
    service.app = app
    
    g_config = config
    host, port = re.split(":")
    app.run(host=host, port=port)