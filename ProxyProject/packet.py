class Packet:
    def __init__(self, packet_type, src_port, dst_port, ack_no, seq_no):
        self.packet = {
            "packet_type": packet_type,
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

    def __repr__(self):
        return f"packet: {self.packet}, data: {self.packet['data']}"

    def __str__(self):
        return f"Type: {self.packet['packet_type']}, src_port: {self.packet['src_port']}, dst_port: " \
               f"{self.packet['dst_port']} ack_no: {self.packet['ack_no']}, seq_no {self.packet['seq_no']}, " \
               f"data: {self.packet['data']}"
