from enum import Enum


class PacketType(Enum):
    DATA = 1
    ACK = 2
    EOF = 3


class Packet:
    def __init__(self, packet_type, sender_ip, receiver_ip, src_port, dst_port, ack_no, seq_no):
        self.packet = {
            "packet_type": packet_type,
            "sender_ip": sender_ip,
            "receiver_ip": receiver_ip,
            "src_port": src_port,
            "dst_port": dst_port,
            "ack_no": ack_no,
            "seq_no": seq_no,
            "data": ""
        }

    def set_data(self, data):
        self.packet['data'] = data

    def add_data(self, data):
        self.packet['data'] += data

    def get_seq(self):
        return self.packet['seq_no']

    def get_ack(self):
        return self.packet['ack_no']

    def get_packet_type(self):
        return self.packet['packet_type'].name
    
    def get_data(self):
        return self.packet['data']

    def __repr__(self):
        return f"packet: Ack: {self.packet['ack_no']}, data_len: {len(self.packet['data'])}"

    def __str__(self):
        return f"Type: {self.packet['packet_type'].name}, src_port: {self.packet['src_port']}, dst_port: " \
               f"{self.packet['dst_port']} ack_no: {self.packet['ack_no']}, seq_no {self.packet['seq_no']}, " \
               f"data: {self.packet['data']}"
