import pickle
import socket
import argparse
from packet import Packet, PacketType
from random import randrange

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

def drop_packet(noise) -> bool:
    drop = False
    
    num = randrange(1, 101)
    if num < int(noise):
        drop = True
    
    return drop


def get_packet(conn) -> list[Packet]:
    while True:
        packet = pickle.loads(conn.recv(SIZE))
        print(f"[PACKET RECEIVED] {packet}\n")
        return packet

'''
This is main of the program.
Parses the command line arguements and creates a socket to start the server.
:raise KeyboardInterrupted: Shuts the server down.
:raise Exception: Shuts the server down.
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, dest='recvIP', required=True) #Should be taking the server's IP address
    parser.add_argument('-rp', type=int, default=PORT, dest='receiverPort')
    parser.add_argument('-sp', type=int, default=PORT, dest='senderPort')
    
    args = parser.parse_args()
    senderAddr = (args.recvIP, args.receiverPort)

    print(f'Starting Proxy Sender on {senderAddr}')
    proxySender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxySender.connect(senderAddr)
    
    # receiverAddr = (get_ip_address(), args.senderPort)
    receiverAddr = ("127.0.0.1", args.senderPort)
    print(f'Starting Proxy Receiver on {receiverAddr}')
    proxyReceiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxyReceiver.bind(receiverAddr)
    proxyReceiver.listen()

    interrupted = False
    
    try:
        dataNoise = input('Enter rate to drop data packets at: \n')
        ackNoise = input('Enter rate to drop ack packets at: \n')

        conn, addr = proxyReceiver.accept()

        while True:
            dataPacket = get_packet(conn)
            while True:
                if not drop_packet(dataNoise):
                    break
                else:
                    print('DATA PACKET DROPPED')
                    dataPacket = get_packet(conn)

            proxySender.send(pickle.dumps(dataPacket))

            ackPacket = get_packet(proxySender)
            if not drop_packet(ackNoise):
                conn.send(pickle.dumps(ackPacket))
            
            else:
                print('ACK PACKET DROPPED')
            if dataPacket.get_packet_type() == PacketType.EOF.name:
                print(f"[EOF DETECTED] Closing connection")
                break
        
        conn.close()

    except KeyboardInterrupt as keyError:
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted

    except Exception as e:
        print(f'\nAn Exception Occured. Shutting Server - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
