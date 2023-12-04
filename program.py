from config_parser import load_config
from multiprocessing import Process
import api 

"""
run flask api server and replica server using process
"""
def run(config:dict):
    p_list = []
    
    for re in config["replicas"]:
        p = Process(target = api.run, args=(re, config, config["replicas"][0], ))
        p_list.append(p)
        p.start()
    
    for p in p_list:
        p.join()


if __name__ == "__main__":
    config = load_config("./config.json")
    if config != None:
        run(config)
    else:
        print("Failed Load Config")