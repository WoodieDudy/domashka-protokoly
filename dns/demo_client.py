import socket

from dnslib import DNSRecord


def main():
    server_address = ("127.0.0.1", 53)
    domain = "github.com"

    query_data = DNSRecord.question(domain, "A").pack()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(query_data, server_address)

    response_data, _ = client_socket.recvfrom(512)
    response = DNSRecord.parse(response_data)

    print(response)
    client_socket.close()


if __name__ == "__main__":
    main()
