import socket
import time
import pickle

from dnslib import DNSRecord, RCODE


class DNSServer:
    def __init__(self):
        self.cache = {}
        self.cache_path = "cache.pickle"


    def load_cache(self):
        try:
            with open(self.cache_path, "rb") as f:
                data = pickle.load(f)
                for key, (record, expiry) in data.items():
                    if time.time() < expiry:
                        self.cache[key] = (record, expiry)
        except FileNotFoundError:
            print("Cache is empty")


    def save_cache(self):
        with open(self.cache_path, "wb") as f:
            pickle.dump(self.cache, f)


    def update_cache(self, key, record, ttl):
        expiry = time.time() + ttl
        self.cache[key] = (record, expiry)


    def get_cached_record(self, key):
        record_data = self.cache.get(key)
        if record_data:
            record, expiry = record_data
            if time.time() < expiry:
                return record
            del self.cache[key]
        return None


    def resolve_query(self, query_data):
        try:
            query = DNSRecord.parse(query_data)
            cached_record = self.get_cached_record(query.q.qname)
            if cached_record:
                return cached_record.pack()

            response = query.send("8.8.8.8", 53)
            response_record = DNSRecord.parse(response)

            if response_record.header.rcode == RCODE.NOERROR:
                for rr in response_record.rr:
                    self.update_cache(rr.rname, response_record, rr.ttl)

            return response
        except Exception as e:
            print(f"Error: {e}")
            return None


def main():
    dns_server = DNSServer()
    dns_server.load_cache()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 53))
    print("DNS server is running...")

    try:
        while True:
            query_data, addr = server_socket.recvfrom(512)
            response_data = dns_server.resolve_query(query_data)
            if response_data:
                server_socket.sendto(response_data, addr)

    except KeyboardInterrupt:
        print("Shutting down the server...")
        dns_server.save_cache()
        server_socket.close()


if __name__ == "__main__":
    main()
