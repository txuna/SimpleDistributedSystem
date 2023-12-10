import json
from multiprocessing import Process
import api_server
import time

def load_config(path:str) -> dict:
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            return data
        
    except Exception as e:
        return None
    

    
def run(config:dict):
    p_list = []
    
    for re in config["replicas"]:
        p = Process(target = api_server.run, args=(re, config, ))
        p_list.append(p)
        p.start()
        time.sleep(1)

    for p in p_list:
        p.join()


if __name__ == "__main__":
    config = load_config("./config.json")
    if config != None:
        run(config)
    else:
        print("Failed Load Config")