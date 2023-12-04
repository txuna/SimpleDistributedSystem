import const
import requests as req
from flask import Blueprint, request
import db
import log

bp = Blueprint('service', __name__, url_prefix='/')


g_config = {}
primary_address = ""
service_address = ""
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# 기존 프라이머리의 데이터베이스 이양
@bp.route("/primary", methods=['GET'])
def relocate_primary():
    return {"res" : const.OK, "st" : db.load_storage()}


@bp.route("/primary/<int:note_id>", methods=['DELETE'])
def forward_request_delete(note_id):
    result = db.delete_note(note_id)
    
    if result == const.FAIL:
        return {"res" : result, "msg" : "Failed Sync"}
    
    sync_db()
    return {"res" : const.OK}  
    

@bp.route("/primary", methods=['POST', 'PUT', 'PATCH'])
def forward_request():
    data = request.get_json()
    result = const.OK

    # 노트 생성하기
    if request.method == 'POST':
        result = db.add_note(data)

    elif request.method == 'PUT':
        result = db.overwrite_note(data)
        
    elif request.method == 'PATCH':
        result = db.modify_note(data)
        
    if result == const.FAIL:
        return {"res" : result, "msg" : "Failed Sync"}

    log.logging_replica("REPLY", "Forward request to primary")
    sync_db()     
    return {"res" : const.OK}  
        

# primary 트래킹 
@bp.route("/backup", methods=['POST', 'PUT', 'PATCH'])
def tell_backup():
    global primary_address
    data = request.get_json()
    db.set_storage(data['storage'])
    primary_address = data['primary']
    return {"res" : const.OK}


def write_post(data):
    if g_config['sync'] == 'remote-write':
        log.logging_replica("REQUEST", "Forward request to primary")
        res = req.post("http://" + primary_address+"/primary", json=data, headers=headers)
        return res.json()
        
    elif g_config['sync'] == 'local-write':
        log.logging_replica("REQUEST", "Move item to new primary")
        res = req.get("http://" + primary_address+"/primary") 
        log.logging_replica("REPLY", "Move item to new primary")
        res = res.json()
        db.set_storage(res['st'])
        result = db.add_note(data)
        if result == const.FAIL:
            return {"res" : const.FAIL, "msg" : "Failed Post"}
        
        sync_db()
        return {"res" : const.OK}
    
    return {"res" : const.FAIL, "msg" : "Failed Post"}


def write_put(data, note_id):
    if g_config['sync'] == 'remote-write':
        data['id'] = note_id
        log.logging_replica("REQUEST", "Forward request to primary")
        res = req.put("http://" + primary_address+"/primary", json=data, headers=headers)
        return res.json()
    
    # primary로부터 데이터베이스를 받는다.
    elif g_config['sync'] == 'local-write':
        log.logging_replica("REQUEST", "Move item to new primary")
        res = req.get("http://" + primary_address+"/primary") 
        log.logging_replica("REPLY", "Move item to new primary")
        res = res.json()
        db.set_storage(res['st'])
        data['id'] = note_id
        result = db.overwrite_note(data)
        if result == const.FAIL:
            return {"res" : const.FAIL, "msg" : "Failed Post"}
        
        sync_db()
        return {"res" : const.OK}

    return {"res" : const.FAIL, "msg" : "Failed Put"}


def write_patch(data, note_id):
    if g_config['sync'] == 'remote-write':
        data['id'] = note_id
        log.logging_replica("REQUEST", "Forward request to primary")
        res = req.patch("http://" + primary_address+"/primary", json=data, headers=headers)
        return res.json()
    
    elif g_config['sync'] == 'local-write':
        log.logging_replica("REQUEST", "Move item to new primary")
        res = req.get("http://" + primary_address+"/primary") 
        log.logging_replica("REPLY", "Move item to new primary")
        res = res.json()
        db.set_storage(res['st'])
        data['id'] = note_id
        result = db.modify_note(data)
        if result == const.FAIL:
            return {"res" : const.FAIL, "msg" : "Failed Post"}
        
        sync_db()
        return {"res" : const.OK}

    return {"res" : const.FAIL, "msg" : "Failed Patch"}


def write_delete(note_id):
    if g_config['sync'] == 'remote-write':
        log.logging_replica("REQUEST", "Forward request to primary")
        res = req.delete("http://" + primary_address+"/primary/"+str(note_id))
        return res.json()
    
    elif g_config['sync'] == 'local-write':
        log.logging_replica("REQUEST", "Move item to new primary")
        res = req.get("http://" + primary_address+"/primary") 
        log.logging_replica("REPLY", "Move item to new primary")
        res = res.json()
        db.set_storage(res['st'])
        result = db.delete_note(note_id)
        if result == const.FAIL:
            return {"res" : const.FAIL, "msg" : "Failed Delete"}
        
        sync_db()
        return {"res" : const.OK}

    return {"res" : const.FAIL, "msg" : "Failed Delete"}


def sync_db():
    data = {
        "storage" : db.load_storage(),
        "primary" : service_address
    }
    
    for re in g_config["replicas"]:
        log.logging_replica("REQUEST", "Tell backups to update")
        res = req.post("http://"+re+"/backup", json=data, headers=headers)
        log.logging_replica("REPLY", "Tell backups to update")


def set_config(cfg):
    global g_config
    g_config = cfg


def set_primary(pa):
    global primary_address
    primary_address = pa
    
    
def set_service_address(adr):
    global service_address
    service_address = adr


def load_note(note_id):
    for note in db.storage['notes']:
        if note['id'] == note_id:
            return note
        
    return None


def load_all_note():
    return db.storage['notes']