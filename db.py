import const


storage = {
    "unique_id" : 1,
    "notes" : []
}


def load_storage():
    global storage
    return storage


def set_storage(st):
    global storage
    storage = st


def add_note(note):
    global storage
    if not "title" in note or not "body" in note:
        return const.FAIL
    
    uuid = storage['unique_id']
    storage['notes'].append({
        'id' : uuid, 
        'title' : note['title'],
        'body' : note['body']
    })
    storage['unique_id'] += 1
    return const.OK


def overwrite_note(data):
    global storage
    for note in storage['notes']:
        if note['id'] == data['id']:
            storage['notes'].remove(note)
            storage['notes'].append(data)
            return const.OK
        
    return const.FAIL            


def modify_note(data):
    global storage
    for note in storage['notes']:
        if note['id'] == data['id']:
            note.update(data)
            return const.OK
        
    return const.FAIL


def delete_note(note_id):
    global storage
    for note in storage['notes']:
        if note['id'] == note_id:
            storage['notes'].remove(note)
            return const.OK
        
    return const.FAIL