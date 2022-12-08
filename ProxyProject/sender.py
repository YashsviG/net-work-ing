from os import path
from GUI import GUI
from packet import Packet, PacketType
import socket
import argparse
import pickle

"""
INITIALIZING GLOBAL VARIABLES
"""
PORT = 5000
FORMAT = 'utf-8'
SIZE = 4096
MSS = 1024
TIMEOUT = 5

countPacketRecvd = 0
countPacketSent = 0

"""
Gets the IP of the sender machine

:return: Returns the IP
"""
def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

"""
Makes the data packet

:param data: Data to add to the packet
:param receiver_ip: IP Address of the receiver machine
:param receiver_port: Port for the receiver machine
:param s_port: Senders port
:param ack: Ack number
:param seq: Sequence number
:return: Returns the created data packet
"""
def makePacket(data, receiver_ip, receiver_port, s_port,  ack, seq) -> Packet:
    s_ip = get_ip_address()
    packet = Packet(PacketType.DATA, s_ip, receiver_ip, s_port, receiver_port, ack, seq)
    packet.add_data(data)
    return packet

"""
Get the list of the data packets

:param string: user's input
:param addr: The address of the sender machine
:param src_port: The port of the sender machine
:return: Returns the list of the data packets
"""
def getPacketList(string, addr, src_port) -> list[Packet]:
    global countPacketSent
    global countPacketRecvd

    packets = []
    ack = 0
    seq = 0
    if not path.exists(string):
        pointer = 0
        while pointer < len(string):
            packets.append(makePacket(string[pointer: pointer+MSS], addr[0], addr[1],src_port, ack, seq))
            ack = 1 if ack == 0 else 0
            seq = 1 if seq == 0 else 0
            pointer += MSS
    else:
        f = open(string, 'r', encoding='utf-8')
        while True:
            d = f.read(MSS)
            if not d:
                break
            packets.append(makePacket(d, addr[0], addr[1], src_port, ack, seq))
            ack = 1 if ack == 0 else 0
            seq = 1 if seq == 0 else 0
        f.close()
    packets.append(Packet(PacketType.EOF, get_ip_address()[0], addr[0], src_port, addr[1], ack, seq))
    return packets

"""
Send the data packets to the connected receiver.

:param conn: Receiver's connected socket to receive data on
:param gui: object of GUI to updata data for the graph
"""
def sendPackets(packets, conn, gui) -> None:
    global countPacketSent
    global countPacketRecvd

    expected_ack = 0
    for i, p in enumerate(packets):
        while True:
            print(f"[SENDING {p.get_packet_type()} PACKET] {p}")
            conn.send(pickle.dumps(p))
            countPacketSent += 1
            if p.get_packet_type() == PacketType.EOF.name:
                print(f"[EOF DETECTED] Closing connection")
                break
            try:
                ack = pickle.loads(conn.recv(SIZE))
                countPacketRecvd += 1
            except socket.timeout:
                print("[TIMEOUT DETECTED]")
                gui.update_data(0)
                pass
            else:
                if ack.get_ack() == expected_ack:
                    gui.update_data(1)
                    break
                else:
                    gui.update_data(0)
                    print(f"[DUPLICATE ACK DETECTED]{ack}")
        expected_ack = 1 if expected_ack == 0 else 0

def show_stats(gui):
    print("===================EOT===================")
    print({"Count of Packets received": countPacketRecvd})
    print({"Counts of Packets sent": countPacketSent})
    print("===================EOT===================")
    gui.draw()
'''
This is main of the program.
Parses the command line arguements and creates a socket to start the sender.
:raise KeyboardInterrupted: Shuts the server down.
:raise Exception: Shuts the server down.
'''
def main() -> None:
    global countPacketSent
    global countPacketRecvd
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, dest='ip', required=True) 
    
    #Should be taking the proxy's IP address no the server directly
    parser.add_argument('-p', type=int, default=PORT, dest='PORT')
    
    args = parser.parse_args()
    addr = (args.ip, args.PORT)

    gui = GUI("Number of Packets sent", "Unique Packets Sent", "Sender Summary")
    interrupted = False
    try:
        print(f'Starting Client on {addr}')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        
        client.settimeout(TIMEOUT)
        
        data = input('Enter file name or a string:')
        
        packets = getPacketList(data, addr, client.getsockname())
        sendPackets(packets, client, gui)

        show_stats(gui)
        client.close()
    except KeyboardInterrupt as keyError:
        show_stats(gui)
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted
    except Exception as e:
        show_stats(gui)
        print(f'\nAn Exception Occured. Shutting Client - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
