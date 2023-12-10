from flask import Flask, request, jsonify
import db_server
import requests as fetch
import const
import log

app = Flask(__name__)
app.register_blueprint(db_server.bp)


# 특정 노트 하나를 읽어옴
@app.route("/note/<int:nid>", methods=['GET'])
def get_one_note(nid):
    log.logging_client("REQUEST", request.method, request.path)
    note = db_server.read(nid)
    res = {}
    if note == None:
        res = {"res" : const.FAIL, "msg" : 'Cannot Found The Note'}
    else:
        res = {"res" : const.OK, 'note' : note}

    log.logging_client("REPLY", request.method, request.path, res)
    return res


# 모든 노트를 읽어옴
@app.route("/note", methods=['GET'])
def get_all_note():
    log.logging_client("REQUEST", request.method, request.path)
    notes = db_server.read(-1)
    log.logging_client("REPLY", request.method, request.path)
    return {"res" : const.OK, "notes" : notes}


# 노트를 추가함 ID는 유니크한 값 - primary에서 제공
@app.route("/note", methods=['POST'])
def create_note():
    body = request.get_json()
    log.logging_client("REQUEST", request.method, request.path, body)
    result = db_server.write('POST', body)
    res = {}
    if result == const.OK:
        res = {"res" : const.OK}
    else:
        res = {"res" : const.FAIL, "msg" : "Cannot Post Note"}
    
    log.logging_client("REPLY", request.method, request.path, res)
    return res


# 노트를 덮어씀
@app.route("/note/<int:nid>", methods=['PUT'])
def overwrite_note(nid):
    body =  request.get_json()
    log.logging_client("REQUEST", request.method, request.path, body)
    result = db_server.write('PUT', body, nid)
    res = {}
    if result == const.OK:
        res = {"res" : const.OK}
    else:
        res = {"res" : const.FAIL, "msg" : "Cannot Put Note"}
    
    log.logging_client("REPLY", request.method, request.path, res)
    return res


# 노트를 수정함
@app.route("/note/<int:nid>", methods=['PATCH'])
def modify_note(nid):
    body =  request.get_json()
    log.logging_client("REQUEST", request.method, request.path, body)
    result = db_server.write('PATCH', body, nid)
    if result == const.OK:
        res = {"res" : const.OK}
    else:
        res = {"res" : const.FAIL, "msg" : "Cannot Patch Note"}
    
    log.logging_client("REPLY", request.method, request.path, res)
    return res


# 노트를 삭제함 
@app.route("/note/<int:nid>", methods=['DELETE'])
def delete_note(nid):
    log.logging_client("REQUEST", request.method, request.path)
    result = db_server.write('DELETE', {}, nid)
    res = {}
    if result == const.OK:
        res = {"res" : const.OK}
    else:
        res = {"res" : const.FAIL, "msg" : "Cannot Delete Note"}
    
    log.logging_client("REPLY", request.method, request.path)
    return res
    

def run(address, config):
    db_server.run(address, config)
    
    host, port = address.split(':')
    app.run(host=host, port=port)