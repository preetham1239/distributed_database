import time

import requests
import yaml

# make a request to the server 1000 times
program_start_time = time.time()
for i in range(100):
    request_start_time = time.time()
    query = "select * from rooms;".lower()
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    port = config['app']['port']
    host = config['app']['host']
    if 'select' in query:
        r = requests.get(f'http://{host}:{port}/databases', data={'query': query, 'api_key': '12345'})
    else:
        r = requests.post('http://{host}:{port}/databases', data={'query': query})
    request_end_time = time.time()
    print(r.content.decode())
    print("Request No. is ", i+1, "and time taken is ", request_end_time - request_start_time, "with status code ", r.status_code)

program_end_time = time.time()
print("Total time taken is ", program_end_time - program_start_time)
