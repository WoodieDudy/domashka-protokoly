import socket
import datetime
import yaml


def time_server(time_offset, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    print(f"Сервер запущен на {host}:{port}")
    print(f"Время смещено на {time_offset} секунд")

    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            current_time = datetime.datetime.now() + datetime.timedelta(seconds=time_offset)
            response = str(current_time).encode('utf-8')
            sock.sendto(response, addr)


def main():
    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    time_offset = config['offset_secs']
    host = config['host']
    port = config['port']

    time_server(time_offset, host, port)

if __name__ == '__main__':
    main()
