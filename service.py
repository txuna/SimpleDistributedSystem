import const

storage = {
    "unique_id" : 1,
    "notes" : []
}


def create_note(note):
    note['id'] = storage['unique_id']
    storage['notes'].append(note)
    storage['unique_id'] += 1
    return const.OK


def delete_note(nid):
    for note in storage['notes']:
        if note['id'] == nid:
            storage['notes'].remove(note)
            return const.OK
        
    return const.FAIL


def overwrite_note(data, nid):
    for note in storage['notes']:
        if note['id'] == nid:
            data['id'] = nid
            storage['notes'].remove(note)
            storage['notes'].append(data)
            return const.OK
        
    return const.FAIL


def modify_note(data, nid):
    for note in storage['notes']:
        if note['id'] == nid:
            note.update(data)
            return const.OK
        
    return const.OK


def load_note(nid=-1):
    if nid == -1:
        return storage['notes']
    
    else:
        for note in storage['notes']:
            if note['id'] == nid:
                return note
        return None   
    
    
def load_unique_id():
    return storage['unique_id']


def update_note(data, nid):
    for note in storage['notes']:
        if note['id'] == nid:
            note.update(data)
            return 
        
    storage['notes'].append(data)
    return


def set_unique_id(uid):
    storage['unique_id'] = uid
    return
