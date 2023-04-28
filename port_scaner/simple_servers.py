import socket
import threading

from time_server import time_server

def run_tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_socket.recv(1024)
        client_socket.close()


if __name__ == '__main__':
    t1 = threading.Thread(target=time_server, args=(1, '127.0.0.1', 1111))
    t2 = threading.Thread(target=run_tcp_server, args=('127.0.0.1', 1112))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
