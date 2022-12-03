import pickle
import socket
import argparse
from packet import Packet, PacketType
from random import randrange
import time

PORT = 5000
SIZE = 4096
FORMAT = 'utf-8'

# GUI DATA
data_packets_dropped = []
ack_packets_dropped = []

countPacketRecvd = 0
countPacketSent = 0
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


def delay_packet(noise) -> bool:
    delay = False

    num = randrange(1, 101)
    if num <= int(noise):
        delay = True

    return delay


def drop_packet(noise) -> bool:
    drop = False

    num = randrange(1, 101)
    if num <= int(noise):
        drop = True

    return drop

# TODO: NEED TO VALIDATE USER INPUTS 
def get_user_data():
    dataNoise = input('Enter rate to drop data packets at: \n')
    ackNoise = input('Enter rate to drop ack packets at: \n')
    delayDataPacket = input('Enter rate to delay data packets at: \n')
    delayAckPacket = input('Enter rate to delay ack packets at: \n')

    return (dataNoise, ackNoise, delayDataPacket, delayAckPacket)


def get_packet(conn) -> list[Packet]:
    global countPacketRecvd

    while True:
        packet = pickle.loads(conn.recv(SIZE))
        print(f"[{packet.get_packet_type()} PACKET RECEIVED] {packet}\n")
        countPacketRecvd += 1
        return packet

def send_packet(proxySender, dataPacket):
    global countPacketSent
    proxySender.send(pickle.dumps(dataPacket))
    countPacketSent += 1
      

'''
This is main of the program.
Parses the command line arguements and creates a socket to start the server.
:raise KeyboardInterrupted: Shuts the server down.
:raise Exception: Shuts the server down.
'''


def main():
    global countPacketSent
    global countPacketRecvd

    parser = argparse.ArgumentParser()
    # Should be taking the server's IP address
    parser.add_argument('-s', type=str, dest='recvIP', required=True)
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
        dataNoise, ackNoise, delayDataPacket, delayAckPacket = get_user_data()

        conn, addr = proxyReceiver.accept()

        while True:
            dataPacket = get_packet(conn)
            if dataPacket.get_packet_type() == PacketType.EOF.name:
                print(f"[EOF DETECTED] Closing connection")
                break

            while True:
                if not drop_packet(dataNoise):
                    data_packets_dropped.append(0)  # GUI
                    break
                else:
                    data_packets_dropped.append(1)  # GUI
                    print('DATA PACKET DROPPED')
                    dataPacket = get_packet(conn)

            if delay_packet(delayDataPacket):
                print("DATA PACKED DELAYED")
                time.sleep(6)

            send_packet(proxySender, dataPacket)
            # proxySender.send(pickle.dumps(dataPacket))
            # countPacketSent += 1

            ackPacket = get_packet(proxySender)
            if not drop_packet(ackNoise):
                ack_packets_dropped.append(0)  # GUI
                if delay_packet(delayAckPacket):
                    print("ACK PACKET DELAYED")
                    time.sleep(6)

                conn.send(pickle.dumps(ackPacket))
                countPacketSent += 1

            else:
                ack_packets_dropped.append(1)  # GUI
                print('ACK PACKET DROPPED')
        
        # to send EOF
        send_packet(proxySender, dataPacket)
   
        # GUI
        print(data_packets_dropped)
        print(ack_packets_dropped)

        print({"Recvd": countPacketRecvd})
        print({"Sent": countPacketSent})

        conn.close()

    except KeyboardInterrupt as keyError:
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted

    except Exception as e:
        print(f'\nAn Exception Occured. Shutting Server - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
