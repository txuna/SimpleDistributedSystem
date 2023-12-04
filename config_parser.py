import json

def load_config(path:str) -> dict:
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            return data
        
    except Exception as e:
        return None