import argparse
from queue import Queue
from socket import AF_INET, gethostbyname, socket, SOCK_STREAM
import threading

def tcp_test(port: int, target_ip: str) -> None:
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Opened Port: {port}")

def worker(target_ip: str, queue: Queue) -> None:
    while not queue.empty():
        port = queue.get()
        tcp_test(port, target_ip)
        queue.task_done()
