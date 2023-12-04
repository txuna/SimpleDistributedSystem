# Simple Distributed System
설정파일에 정의된 API 서버와 연결된 데이터베이스를 PRIMARY BASE를 기반으로 한 분산시스템

## Architecture
API 서버와 데이터베이스간의 2가지의 동기화 메커니즘을 구현하였습니다. 

### primary base - remote write 


### primary base - local write 



## Dependency 
- Python 3.10 이상
- pip 패키지 관리 도구
```Shell
pip install flask 
pip install requests
pip install json
```

## How to execute
config.json 파일을 편집하여 최대 REPLICA의 갯수 및 포트 설정이 가능합니다.
```python
{
    "service" : 9988, 
    "sync" : "remote-write", 
    "replicas" : [
        "127.0.0.1:10000", 
        "127.0.0.1:20000",
        "127.0.0.1:30000",
        "127.0.0.1:40000"
    ]
}
```

```Shell
python3 program.py
```

# Remote Write 
### POST NOTE
```SHELL
[2023-12-04 20:58:53] CLIENT [REQUEST] [POST] /note [{'title': 'Hello World', 'body': 'this is new note'}]
[2023-12-04 20:58:53] REPLICA [REQUEST] Forward request to primary
[2023-12-04 20:58:53] REPLICA [REPLY] Forward request to primary
[2023-12-04 20:58:53] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:58:53] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:58:53] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:58:53] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:58:53] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:58:53] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:58:53] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:58:53] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:58:53] CLIENT [REPLY] [POST] /note [{'res': 200}]
```

### PATCH NOTE
```SHELL
[2023-12-04 20:59:09] CLIENT [REQUEST] [PATCH] /note/1 [{'title': 'Hello World', 'body': 'patch note'}]
[2023-12-04 20:59:09] REPLICA [REQUEST] Forward request to primary
[2023-12-04 20:59:09] REPLICA [REPLY] Forward request to primary
[2023-12-04 20:59:09] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:09] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:09] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:09] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:09] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:09] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:09] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:09] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:09] CLIENT [REPLY] [PATCH] /note/1 [{'res': 200}]
```

### PUT NOTE
```SHELL
[2023-12-04 20:59:23] CLIENT [REQUEST] [PUT] /note/1 [{'title': 'Hello World'}]
[2023-12-04 20:59:23] REPLICA [REQUEST] Forward request to primary
[2023-12-04 20:59:24] REPLICA [REPLY] Forward request to primary
[2023-12-04 20:59:24] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:24] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:24] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:24] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:24] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:24] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:24] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:24] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:24] CLIENT [REPLY] [PUT] /note/1 [{'res': 200}]
```

### DELETE NOTE
```SHELL
[2023-12-04 20:59:28] CLIENT [REQUEST] [DELETE] /note/1 [{}]
[2023-12-04 20:59:28] REPLICA [REQUEST] Forward request to primary
[2023-12-04 20:59:28] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:28] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:28] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:28] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:28] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:28] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:28] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:59:28] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:59:28] CLIENT [REPLY] [DELETE] /note/1 [{'res': 200}]
```

### GET ALL NOTE
```SHELL
[2023-12-04 20:59:39] CLIENT [REQUEST] [GET] /note [{}]
[2023-12-04 20:59:39] CLIENT [REPLY] [GET] /note [{'res': 200, 'data': []}]
```

# Local Write
### POST NOTE
```SHELL
[2023-12-04 20:53:36] CLIENT [REQUEST] [POST] /note [{'title': 'Hello World', 'body': 'new note gug123u'}]
[2023-12-04 20:53:36] REPLICA [REQUEST] Move item to new primary
[2023-12-04 20:53:36] REPLICA [REPLY] Move item to new primary
[2023-12-04 20:53:36] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:36] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:36] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:36] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:36] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:36] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:36] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:36] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:36] CLIENT [REPLY] [POST] /note [{'res': 200}]
```
### GET SPECIFIC NOTE
```SHELL
[2023-12-04 20:53:44] CLIENT [REQUEST] [GET] /note/1 [{}]
[2023-12-04 20:53:44] CLIENT [REPLY] [GET] /note/1 [{'res': 200, 'note': {'id': 1, 'title': 'Hello World', 'body': 'new note gug123u'}}]
```

### PATCH NOTE
```SHELL
[2023-12-04 20:53:59] CLIENT [REQUEST] [PATCH] /note/1 [{'title': 'Hello World', 'body': 'patch note'}]
[2023-12-04 20:53:59] REPLICA [REQUEST] Move item to new primary
[2023-12-04 20:53:59] REPLICA [REPLY] Move item to new primary
[2023-12-04 20:53:59] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:59] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:59] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:59] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:59] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:59] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:59] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:53:59] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:53:59] CLIENT [REPLY] [PATCH] /note/1 [{'res': 200}]
```

### PUT NOTE
```SHELL
[2023-12-04 20:54:08] CLIENT [REQUEST] [PUT] /note/1 [{'title': 'Hello World'}]
[2023-12-04 20:54:08] REPLICA [REQUEST] Move item to new primary
[2023-12-04 20:54:08] REPLICA [REPLY] Move item to new primary
[2023-12-04 20:54:08] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:08] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:08] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:08] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:08] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:08] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:08] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:08] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:08] CLIENT [REPLY] [PUT] /note/1 [{'res': 200}]
```

### DELETE NOTE
```SHELL
[2023-12-04 20:54:12] CLIENT [REQUEST] [DELETE] /note/1 [{}]
[2023-12-04 20:54:12] REPLICA [REQUEST] Move item to new primary
[2023-12-04 20:54:12] REPLICA [REPLY] Move item to new primary
[2023-12-04 20:54:12] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:12] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:12] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:12] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:12] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:12] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:12] REPLICA [REQUEST] Tell backups to update
[2023-12-04 20:54:12] REPLICA [REPLY] Tell backups to update
[2023-12-04 20:54:12] CLIENT [REPLY] [DELETE] /note/1 [{'res': 200}]
```

### GET ALL NOTE
```SHELL
[2023-12-04 20:54:23] CLIENT [REQUEST] [GET] /note [{}]
[2023-12-04 20:54:23] CLIENT [REPLY] [GET] /note [{'res': 200, 'data': []}]
```

### Performance