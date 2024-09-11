import requests, json, threading, time

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

    threads = []
    for n in range(1, number+1):
        thread = threading.Thread(target=write_to_json, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with open('data.json', 'a') as file:
        file.write(']')

    end_time = time.time()
    print(end_time - start_time)

extract_data(77)
