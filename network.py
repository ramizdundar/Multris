import pickle
import socket
import subprocess
import threading
from concurrent.futures.thread import ThreadPoolExecutor

from constants import local_port, buffer_size
from packet import Packet, PacketType


class Network:
    local_ip = ""
    # IP of the other player
    remote_ip = ""

    def __init__(self, name="Unanimous"):
        self.executor = ThreadPoolExecutor()

        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_server_socket.bind((self.local_ip, local_port))
        self.udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        Packet.name = name
        self.local_ip = self.get_ip()
        self.remote_address = None
        self.shutdown = False

    @staticmethod
    def get_ip():
        cmd_get_ip = "ifconfig | grep netmask"
        out, err = subprocess.Popen(cmd_get_ip, shell=True, stdout=subprocess.PIPE).communicate()
        ifconfig_lines = out.decode("utf-8").split("\n")[:-1]
        ifconfig_ips = [line.split()[1] for line in ifconfig_lines if line.split()[1] != "127.0.0.1"]
        return ifconfig_ips[0]

    # Do not call this function explicitly. Instead call run() below.
    def udp_server(self):
        while not self.shutdown:
            bytes_packet_address_pair = self.udp_server_socket.recvfrom(buffer_size)
            bytes_packet = bytes_packet_address_pair[0]
            address = bytes_packet_address_pair[1]
            self.executor.submit(self.handle_udp_packet, bytes_packet, address)

    def send_udp_packet(self, packet, address):
        bytes_packet = pickle.dumps(packet)
        self.executor.submit(self.udp_client_socket.sendto, bytes_packet, address)

    def discover(self):
        packet = Packet(PacketType.DISCOVER)
        # address = ("<broadcast>", local_port) TODO: Fix broadcast
        address = ("192.168.1.8", local_port)
        self.send_udp_packet(packet, address)
        self.send_udp_packet(packet, address)
        self.send_udp_packet(packet, address)

    def run(self):
        udp_server_thread = threading.Thread(target=self.udp_server)
        udp_server_thread.start()

    def handle_udp_packet(self, bytes_packet, address):
        packet = pickle.loads(bytes_packet)
        if packet.packet_type == PacketType.DISCOVER:
            self.remote_ip = address[0]
            self.remote_address = (self.remote_ip, local_port)
            self.send_udp_packet(Packet(PacketType.RESPOND), address)
        if packet.packet_type == PacketType.RESPOND:
            self.remote_ip = address[0]
            self.remote_address = (self.remote_ip, local_port)
            print(self.remote_address)
        if packet.packet_type == PacketType.QUIT:
            self.shutdown = True
