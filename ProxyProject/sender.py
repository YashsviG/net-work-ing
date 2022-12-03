from os import path
from packet import Packet, PacketType
import socket
import argparse
import pickle

PORT = 5000
FORMAT = 'utf-8'
SIZE = 4096
MSS = 1
TIMEOUT = 5

countPacketRecvd = 0
countPacketSent = 0

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def makePacket(data, receiver_ip, receiver_port, s_port,  ack, seq) -> Packet:
    s_ip = get_ip_address()
    packet = Packet(PacketType.DATA, s_ip, receiver_ip, s_port, receiver_port, ack, seq)
    packet.add_data(data)
    return packet


def getPacketList(string, addr, src_port):
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


def sendPackets(packets, conn):
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
                pass
            else:
                if ack.get_ack() == expected_ack:
                    break
                
                else:
                    print(f"[DUPLICATE ACK DETECTED]{ack}")
           
        expected_ack = 1 if expected_ack == 0 else 0


def main() -> None:
    global countPacketSent
    global countPacketRecvd
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, dest='IP', required=True) #Should be taking the proxy's IP address no the server directly
    parser.add_argument('-p', type=int, default=PORT, dest='PORT')
    
    args = parser.parse_args()
    addr = (args.IP, args.PORT)
    
    interrupted = False
    try:
        print(f'Starting Client on {addr}')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        
        client.settimeout(TIMEOUT)
        
        data = input('Enter file name or a string:')
        
        packets = getPacketList(data, addr, client.getsockname())
        sendPackets(packets, client)
        
        print({"Recvd": countPacketRecvd})
        print({"Sent": countPacketSent})
        client.close()
    except KeyboardInterrupt as keyError:
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted
    except Exception as e:
        print(f'\nAn Exception Occured. Shutting Client - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
