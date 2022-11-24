import socket
import hashlib
from multiprocessing import Process
import math
import json
import sys

sample_space = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def int_to_str(num):
    final_str = ''
    sample_length = len(sample_space)
    for i in range(5):
        num1 = num % sample_length
        num = int((num - num1) / sample_length)
        final_str += sample_space[num1]
    return final_str[::-1]


def get_password(num_worker, wid, md5hash, connection):
    end_num = math.pow(len(sample_space), 5) - 1
    password_str = ''
    for i in range(wid, int(end_num), num_worker):
        password_str = int_to_str(i)
        password_md5 = hashlib.md5(password_str.encode('utf-8'))
        # print(password_str)
        if md5hash == password_md5.hexdigest():
            break
    connection.sendall(password_str.encode())
    connection.close()


def main_client(Host, Port_num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((Host, Port_num))
    s.listen()
    processes = []
    while True:
        connection, address = s.accept()
        print('Connected by', address)
        while True:
            data = connection.recv(1024)
            message = json.loads(data.decode())
            numw = message['num_worker']
            wid = message['wid']
            md5hash = message['hash']
            if message['status']:
                client_process = Process(target=get_password, args=(numw, wid, md5hash, connection))
                processes.append(client_process)
                client_process.start()
            else:
                for process in processes:
                    if process.is_alive():
                        process.terminate()
                processes = []
                break


if __name__ == "__main__":
    # server_name, server_port = sys.argv[1], int(sys.argv[2])
    server_name = sys.argv[1]
    server_port = 3888
    main_client(server_name, server_port)
