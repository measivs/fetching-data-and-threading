import requests, json, threading, time
from concurrent.futures import ThreadPoolExecutor

file_lock = threading.Lock()
first_object = [True]

def write_to_json(n):
    url = f"https://jsonplaceholder.typicode.com/posts/{n}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()

        with file_lock:
            with open('data.json', 'a') as file:
                if not first_object[0]:
                    file.write(',\n')
                json.dump(data, file, indent=4)
                first_object[0] = False

def extract_data(number):
    start_time = time.time()

    with open('data.json', 'w') as file:
        file.write('[')

    with ThreadPoolExecutor() as executor:
        executor.map(write_to_json, range(1, number+1))

    with open('data.json', 'a') as file:
        file.write(']')

    end_time = time.time()
    print(end_time - start_time)

extract_data(77)
