import time

import requests

# make a request to the server 1000 times
program_start_time = time.time()
for i in range(1):
    request_start_time = time.time()
    query = "select * from rooms".lower()
    if 'select' in query:
        r = requests.get('http://localhost:5000/databases', data={'query': query})
    else:
        r = requests.post('http://localhost:5000/databases', data={'query': query})
    request_end_time = time.time()
    print(r.content.decode())
    print("Request No. is ", i+1, "and time taken is ", request_end_time - request_start_time, "with status code ", r.status_code)

program_end_time = time.time()
print("Total time taken is ", program_end_time - program_start_time)
