import socket
import datetime
import time

import yaml


with open('config.yaml') as f:
    config = yaml.safe_load(f)

SERVER_HOST = config['host']
SERVER_PORT = config['port']

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto(b'request', (SERVER_HOST, SERVER_PORT))
    request_time = datetime.datetime.now()
    data, addr = sock.recvfrom(1024)

    if data:
        response_time = data.decode('utf-8')
        server_time = datetime.datetime.strptime(response_time, '%Y-%m-%d %H:%M:%S.%f')
        print(f"Время запроса: {request_time}")
        print(f"Полученное время: {server_time}")
        print(f"Разница: {server_time - request_time}")
        print()
    time.sleep(5)
