import service
from flask import Blueprint, request
import requests as fetch
import const
import service
import log

bp = Blueprint('db_server', __name__, url_prefix='/')

g_config = {}
# 자신의 주소
g_address = ""
# primary의 주소
g_paddr = ""


# only remote write 
# to do sync
@bp.route("/primary", methods=['POST'])
def forward_primary():
    body = request.get_json()
    res = service.create_note(body)
    log.logging_replica("REPLY", "Forward request to primary")
    if res == const.OK:
        sync(body, service.load_unique_id())
        
    return {"res" : res}

# only remote write
# to do sync 
@bp.route("/primary/<int:nid>", methods=['DELETE', 'PUT', 'PATCH'])
def forward_primary_id(nid):
    if request.method == 'DELETE':
        res = service.delete_note(nid)
        if res == const.OK:
            sync_id(request.method, service.load_unique_id(), nid, {})
            
        return {"res" : res}
    
    elif request.method == 'PUT':
        body = request.get_json()
        res = service.overwrite_note(body, nid)
        if res == const.OK:
            sync_id(request.method, service.load_unique_id(), nid, body)
            
        return {"res" : res}
    
    elif request.method == 'PATCH':
        body = request.get_json()
        res = service.modify_note(body, nid)
        if res == const.OK:
            sync_id(request.method, service.load_unique_id(), nid, body)

        return {"res" : res}

    return {"res" : const.FAIL}


# remote-write, local-write 공유 
# primary tracking
@bp.route("/backup", methods=['POST'])
def tell_backup():
    global g_paddr
    body = request.get_json()
    g_paddr = body['primary']
    res = service.create_note(body['note'])
    return {"res" : res}


# remote-write, local-write 공유 
# primary tracking
@bp.route("/backup/<int:nid>", methods=['DELETE', 'PUT', 'PATCH'])
def tell_backup_id(nid):
    global g_paddr
    body = request.get_json()
    note = body['note']
    g_paddr = body['primary']
    
    if request.method == 'DELETE':
        res = service.delete_note(nid)
        return {"res" : res}
    
    elif request.method == 'PUT':
        res = service.overwrite_note(note, nid)
        return {"res" : res}
    
    elif request.method == 'PATCH':
        res = service.modify_note(note, nid)
        return {"res" : res}
    
    return {"res" : const.FAIL}


# only local write
@bp.route("/primary/<int:nid>", methods=['GET'])
def move_item_id(nid):
    note = service.load_note(nid)
    return {'res' : const.OK, 'note' : note}


def sync(note, uid):
    data = {
        'note' : note, 
        'uid' : uid, 
        'primary' : g_address
    }
    
    log.logging_replica("REQUEST", "Tell backups to update")
    for re in g_config['replicas']:
        if re == g_paddr:
            continue
        res = fetch.post("http://" + re+"/backup", json=data, headers=const.headers)
        
    log.logging_replica("REPLY", "Tell backups to update")
    return const.OK


def sync_id(method, uid, nid, note={}):
    data = {
        'note' : note, 
        'uid' : uid,
        'primary' : g_address
    }
    
    log.logging_replica("REQUEST", "Tell backups to update")
    for re in g_config['replicas']:
        if re == g_paddr:
            continue
        
        if method == 'DELETE':
            res = fetch.delete("http://" + re + "/backup/" + str(nid), json=data, headers=const.headers)
        
        elif method == 'PATCH':
            res = fetch.patch("http://" + re + "/backup/" + str(nid), json=data, headers=const.headers)
        
        elif method == 'PUT':
            res = fetch.put("http://" + re + "/backup/" + str(nid), json=data, headers=const.headers)
    
    log.logging_replica("REPLY", "Tell backups to update")
    return const.OK



def write(method, note={}, nid=-1) -> bool:
    # remote-write의 primary에게 데이터를 전송한다. 
    global g_paddr
    result = const.OK
    if g_config['sync'] == 'remote-write':
        if method == 'POST':
            result = write_post(note)
        
        elif method == 'PATCH':
            result = write_patch(note, nid)
        
        elif method == 'PUT':
            result = write_put(note, nid)
        
        elif method == 'DELETE':
            result = write_delete(nid)
    
    # local-write의 경우 기존 primary로부터 데이터를 받아와서 자신이 primary가 된다.
    elif g_config['sync'] == 'local-write':
        # primary 자신으로 변경
        g_paddr = g_address
        # 새로운 노트를 만든다는 primary에게도 없다는 것인데 요청하는 것이 맞을까 
        if method == 'POST':
            result = write_post(note)
            if result == const.OK:
                sync(note, service.load_unique_id())
        
        else:
            log.logging_replica("REQUEST", "Move item to new primary")
            res = fetch.get("http://" + g_paddr + "/primary/" + str(nid)) 
            log.logging_replica("REPLY", "Move item to new primary")
            data = res.json()
            # primary로부터 가지고온 노트를 업데이트
            service.update_note(data['note'], nid)
            
            if method == 'DELETE':
                result = write_delete(nid)
                if result == const.OK:
                    sync_id(request.method, service.load_unique_id(), nid, {})
            
            elif method == 'PUT':
                result = write_put(note, nid)
                if result == const.OK:
                    sync_id(request.method, service.load_unique_id(), nid, note)
            
            elif method == 'PATCH':
                result = write_patch(note, nid)
                if result == const.OK:
                    sync_id(request.method, service.load_unique_id(), nid, note)
                
    return result
    

def read(nid):
    return service.load_note(nid)


def write_post(note) -> bool:
    if g_config['sync'] == 'remote-write':
        log.logging_replica("REQUEST", "Forward request to primary")
        res = fetch.post("http://" + g_paddr+"/primary", json=note, headers=const.headers)
        result = res.json()
        return result['res']
    
    # local-write
    else:
        res = service.create_note(note)
        return res
    
    
def write_delete(nid):
    if g_config['sync'] == 'remote-write':
        log.logging_replica("REQUEST", "Forward request to primary")
        res = fetch.delete("http://" + g_paddr+"/primary/" + str(nid))
        result = res.json()
        return result['res']

    #local-write
    else:
        res = service.delete_note(nid)
        return res


def write_put(note, nid):
    if g_config['sync'] == 'remote-write':
        log.logging_replica("REQUEST", "Forward request to primary")
        res = fetch.put("http://" + g_paddr+"/primary/" + str(nid), json=note, headers=const.headers)
        result = res.json()
        return result['res']

    #local-write
    else:
        res = service.overwrite_note(note, nid)
        return res


def write_patch(note, nid):
    if g_config['sync'] == 'remote-write':
        log.logging_replica("REQUEST", "Forward request to primary")
        res = fetch.patch("http://" + g_paddr+"/primary/" + str(nid), json=note, headers=const.headers)
        result = res.json()
        return result['res']

    #local-write
    else:
        res = service.modify_note(note, nid)
        return res


def run(address, config):
    global g_config, g_address, g_paddr
    
    g_address = address
    g_config = config
    g_paddr = config["replicas"][0]
    
    # primary로 부터 데이터를 받아옴
    if g_address != g_paddr:
        pass