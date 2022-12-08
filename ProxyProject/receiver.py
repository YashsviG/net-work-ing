import pickle
import socket
import argparse
from GUI import GUI
from packet import Packet, PacketType

"""
INITIALIZING GLOBAL VARIABLES
"""
PORT = 5000
BUFFER_SIZE = 4096
FORMAT = 'utf-8'

countOfPacketRecvd = 0
countOfPacketSent = 0

"""
Gets the IP of the receiver machine

:return: Returns the IP
"""
def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

"""
Makes the ack packet for the received data packet

:param addr: Address of the connected sender
:param recv_info: Address of the receiver machine
:param ack: Ack number
:param seq: Sequence number
:return: Returns the created ack packet
"""
def makePacket(addr, recv_info, ack, seq) -> Packet:
    ack_no = ack
    seq_no = seq
    packet = Packet(PacketType.ACK, recv_info[0], addr[0], recv_info[1], addr[1], ack_no, seq_no)
    return packet

"""
Gets the data packets

:param conn: Receiver's connected socket to receive data on
:param addr: Address of the connected sender
:param recv_info: Address of the receiver machine
:param gui: object of GUI to updata data for the graph
:return: Returns the received list of unqiue Data packets
"""
def get_packets(conn, addr, recv_info, gui) -> list[Packet]:
    global countOfPacketSent
    global countOfPacketRecvd

    packets = []
    seq = 0
    ack = 1
    while True:
        packet = pickle.loads(conn.recv(BUFFER_SIZE))
        countOfPacketRecvd += 1
        print(f"[{packet.get_packet_type()} PACKET RECEIVED] {packet}\n")
        
        if packet.get_packet_type() == PacketType.EOF.name:
            print(f"[EOF DETECTED] Closing connection")
            break
        
        new_ack = packet.get_seq()
        if not ack == new_ack:
            ack = new_ack
            packets.append(packet.get_data())
            ackpack = makePacket(addr, recv_info, ack, seq)
            gui.update_data(1)
            print(f"[Sending ACK] {ackpack}")
            conn.send(pickle.dumps(ackpack))
            countOfPacketSent += 1
        else:
            print("DUPLICATE DATA PACKET DETECTED")
            print(f"[Sending DUP ACK] {ackpack}")
            gui.update_data(0)
            conn.send(pickle.dumps(ackpack))
            countOfPacketSent += 1
        seq = 1 if seq == 0 else 0
    return packets

'''
This is main of the program.
Parses the command line arguements and creates a socket to start the receiver.
:raise KeyboardInterrupted: Shuts the server down.
:raise Exception: Shuts the server down.
'''
def main() -> None:
    global countOfPacketRecvd
    global countOfPacketSent

    gui = GUI("Number of Acks packets sent", "Unique ACKs Sent", "Receiver Summary")
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
        get_packets(conn, addr, recv_info, gui)

        print("===================EOT===================")
        print("STATS - RECEIVER")
        print({"Count of Packets received": countOfPacketRecvd})
        print({"Counts of Packets sent": countOfPacketSent})
        print("===================EOT===================")
        conn.close()
        gui.draw()
    except KeyboardInterrupt as keyError:
        print("===================EOT===================")
        print("STATS - RECEIVER")
        print({"Count of Packets received": countOfPacketRecvd})
        print({"Counts of Packets sent": countOfPacketSent})
        print("===================EOT===================")
        gui.draw()
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted
    except Exception as e:
        print("===================EOT===================")
        print("STATS - RECEIVER")
        print({"Count of Packets received": countOfPacketRecvd})
        print({"Counts of Packets sent": countOfPacketSent})
        print("===================EOT===================")
        gui.draw()
        print(f'\nAn Exception Occured. Shutting Server - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
