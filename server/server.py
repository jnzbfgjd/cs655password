from flask import Flask, render_template, request
import socket
import time
import json
import multiprocessing

app = Flask(__name__)
host_list = []
port_list = [3888, 3888, 3888, 3888]


@app.route('/')
def startup():
    return render_template('password.html')


@app.route('/', methods=['POST', 'GET'])
def interface():
    if request.method == 'POST':
        # These are the input fields that we get from the user filling out the form on the web interface.
        hash_to_crack = request.form['hash']
        numWorkers = request.form['workers']

        begin_time = time.time()
        response = multi_socket(hash_to_crack, numWorkers)
        end_time = time.time()

        # response = data.decode()
        t = end_time - begin_time

        # Render the form with the response from the master node included
        return render_template('password.html', cracked=response, time=t)


def multi_socket(hash_to_crack, numWorkers):
    processes = []
    numWorkers = int(numWorkers)
    manager = multiprocessing.Manager()
    return_code = manager.list()
    socket_list = manager.list()
    for i in range(numWorkers):
        process = multiprocessing.Process(
            target=one_socket_process, args=(hash_to_crack, numWorkers, i, return_code, socket_list)
        )
        processes.append(process)
        process.start()

    while True:
        if len(return_code) != 0:
            for process in processes:
                process.terminate()
            for s in socket_list:
                message = json.dumps({'status': False, 'num_worker': int(numWorkers), 'wid': 0, 'hash': 0})
                s.sendall(message.encode())
                print('send terminate message')
                s.close()
            break
    return return_code[0]


def one_socket_process(hash_to_crack, numWorkers, wid, return_code, socket_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = host_list[wid]
    PORT_NUM = port_list[wid]
    s.connect((HOST, PORT_NUM))
    socket_list.append(s)
    message = json.dumps({'status': True, 'num_worker': int(numWorkers), 'wid': wid, 'hash': hash_to_crack})
    s.sendall(message.encode())
    data = s.recv(1024)
    print('worker with ' + str(wid) + ' return the result')
    return_code.append(data.decode())


def read_txt(file_path):
    with open(file_path, encoding='utf-8') as file:
        content = file.readlines()
    return content


if __name__ == "__main__":
    c0 = read_txt('./workerhost.txt')
    c1 = read_txt('./managerhost.txt')
    for line in c0:
        host_list.append(line.replace('\n', ''))
    print(host_list)
    for line in c1:
        local_host = line.replace('\n', '')
    print(local_host)
    app.run(host=local_host, port=3890, debug=False)
