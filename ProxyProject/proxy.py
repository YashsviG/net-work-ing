import pickle
import socket
import argparse

from GUI import GUI, draw
from packet import Packet, PacketType
from random import randrange
import time
import json

"""
INITIALIZING GLOBAL VARIABLES
"""
PORT = 5000
SIZE = 4096
FORMAT = 'utf-8'

countPacketRecvd = 0
countPacketSent = 0




"""
Gets the IP of the proxy machine        

:return: Returns the IP address of the machine    
"""
def get_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

"""
Gets the data from the config json based on the key provided

:param key: key to retrieve data from the config file
:return: int - drop/delay rate for the key
"""
def get_drop_delay(key) -> int:
    f = open("config.json", "r")
    f = json.load(f)
    return int(f[key])

"""
Calculates the chances of delaying the data or ack packet

:param noise: percent rate to delay the packet.
:return: Boolean to either delay or not delay the packet
"""
def delay_packet(noise) -> bool:
    delay = False

    num = randrange(1, 101)
    if num <= int(noise):
        delay = True

    return delay


"""
Calculates the chances of dropping the data or ack packet

:param noise: percent rate to drop the packet.
:return: Boolean to either drop or not drop the packet
"""
def drop_packet(noise) -> bool:
    drop = False

    num = randrange(1, 101)
    if num <= int(noise):
        drop = True

    return drop


"""
Receives the packet from the receiver and the sender

:param conn: socket connection to receive data on
:return: lists of packets received
"""
def get_packet(conn) -> Packet:
    global countPacketRecvd

    while True:
        packet = pickle.loads(conn.recv(SIZE))
        print(f"[{packet.get_packet_type()} PACKET RECEIVED] {packet}\n")
        countPacketRecvd += 1
        return packet


"""
Sends the packet to the receiver

:param proxySender: socket connection to send data on
:param dataPacket: 
:return: lists of packets received
"""
def send_packet(proxySender, dataPacket) -> None:
    global countPacketSent
    proxySender.send(pickle.dumps(dataPacket))
    countPacketSent += 1


'''
This is main of the program.
Parses the command line arguements and creates a socket to start the proxy receiver 
and the sender and calls the functions appropriately to drop/delay packets received 
on the sockets and lists the stats at the end.

:raise KeyboardInterrupted: Shuts the server down.
:raise Exception: Shuts the server down.
'''
def main() -> None:
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
    ack_gui = GUI("Number of Acks Received", "ACKs Dropped", "Proxy Summary")
    data_gui = GUI("Number of Data Received", "Data packet Dropped", "")
    gui_list = [ack_gui, data_gui]
    try:
        conn, addr = proxyReceiver.accept()

        while True:
            data_packet = get_packet(conn)
            if data_packet.get_packet_type() == PacketType.EOF.name:
                print(f"[EOF DETECTED] Closing connection")
                break

            while True:
                if not drop_packet(get_drop_delay("data_packet_drop")):
                    break
                else:
                    data_gui.update_data(1)
                    print('DATA PACKET DROPPED')
                    data_packet = get_packet(conn)
            if delay_packet(get_drop_delay("data_packet_delay")):
                print("DATA PACKED DELAYED")
                time.sleep(6)
            data_gui.update_data(0)

            send_packet(proxySender, data_packet)

            ackPacket = get_packet(proxySender)
            if not drop_packet(get_drop_delay("ack_packet_drop")):
                if delay_packet(get_drop_delay("ack_packet_delay")):
                    print("ACK PACKET DELAYED")
                    time.sleep(6)
                ack_gui.update_data(0)
                conn.send(pickle.dumps(ackPacket))
                countPacketSent += 1

            else:
                ack_gui.update_data(1)
                print('ACK PACKET DROPPED')

        # to send EOF
        send_packet(proxySender, data_packet)

        print("===================EOT===================")
        print("STATS - PROXY")
        print({"Count of Packets received": countPacketRecvd})
        print({"Counts of Packets sent": countPacketSent})
        print("===================EOT===================")

        conn.close()
        draw(gui_list)
    except KeyboardInterrupt as keyError:
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted
    except Exception as e:
        print(f'\nAn Exception Occured. Shutting Server - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
