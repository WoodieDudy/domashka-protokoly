import socket
import threading
import argparse
from queue import Queue

def tcp_scan(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        return True
    except:
        return False
    finally:
        s.close()


def udp_scan(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)

    try:
        s.sendto(b'test_data', (ip, port))
        s.recvfrom(1024)
        return True
    except socket.timeout:
        return False
    except:
        return True
    finally:
        s.close()


def worker(q, ip):
    while not q.empty():
        port = q.get()
        if tcp_scan(ip, port):
            print(f'TCP port {port} is open')
        if udp_scan(ip, port):
            print(f'UDP port {port} is open')


def main(ip, start_port, end_port, threads_count):
    q = Queue()
    for port in range(start_port, end_port + 1):
        q.put(port)

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=worker, args=(q, ip))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='IP address to scan')
    parser.add_argument('start_port', type=int, help='Start port to scan')
    parser.add_argument('end_port', type=int, help='End port to scan')
    parser.add_argument('-t', '--threads', type=int, default=10,
                        help='Number of threads')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.ip, args.start_port, args.end_port, args.threads)
