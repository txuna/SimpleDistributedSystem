from datetime import datetime

def logging_client(type, method, uri, data={}):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('./log/log.txt', 'a') as file:
        content = f"[{timestamp}] CLIENT [{type}] [{method}] {uri} [{data}]\n"
        file.write(content)
        
        
def logging_replica(type, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('./log/log.txt', 'a') as file:
        content = f"[{timestamp}] REPLICA [{type}] {msg}\n"
        file.write(content)