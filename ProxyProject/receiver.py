import pickle
import socket
import argparse
from packet import Packet, PacketType

PORT = 5000
SIZE = 4096
FORMAT = 'utf-8'

"""
Gets the IP of the server machine

:return: Returns the IP
"""


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def makePacket(addr, recv_info, ack, seq) -> Packet:
    ack_no = ack
    seq_no = seq
    packet = Packet(PacketType.ACK, recv_info[0], addr[0], recv_info[1], addr[1], ack_no, seq_no)
    return packet


def get_packets(conn, addr, recv_info) -> list[Packet]:
    packets = []
    seq = 0
    while True:
        packet = pickle.loads(conn.recv(SIZE))
        print(f"[PACKET RECEIVED] {packet}\n")
        packets.append(packet)
        if packet.get_packet_type() == PacketType.EOF.name:
            print(f"[EOF DETECTED] Closing connection")
            break
        ack = packet.get_seq()
        ackpack = makePacket(addr, recv_info, ack, seq)
        print(f"[Sending ACK] {ackpack}")
        conn.send(pickle.dumps(ackpack))
        seq = 1 if seq == 0 else 0
    return packets

'''
This is main of the program.
Parses the command line arguements and creates a socket to start the server.
:raise KeyboardInterrupted: Shuts the server down.
:raise Exception: Shuts the server down.
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=PORT, dest='port')
    args = parser.parse_args()
    ip = get_ip_address()
    recv_info = (ip, args.port)

    print(f'Starting Server on {recv_info}')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(recv_info)
    server.listen()

    interrupted = False
    try:
        conn, addr = server.accept()
        packets = get_packets(conn, addr, recv_info)
        conn.close()
    except KeyboardInterrupt as keyError:
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted
    # except Exception as e:
    #     print(f'\nAn Exception Occured. Shutting Server - {repr(e)}')
    #     assert not interrupted


if __name__ == '__main__':
    main()
