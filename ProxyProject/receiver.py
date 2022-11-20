from genericpath import exists
import socket
import argparse
import os
import re as regex
import Packet

PORT = 5000
SIZE = 1024
FORMAT = 'utf-8'

'''
Gets the IP of the server machine

:return: Returns the IP
'''
def getIP():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0)
    try:
        sock.connect(('10.254.254.254', 80))
        IP = sock.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        sock.close()
    return IP

def makePacket(data, ackN, seqN) -> Packet:
    packet_type = 'ack'
    src_port = 5000
    dest_port = 5000
    ack_no = ackN
    seq_no = seqN
    data = data
    packet = Packet(packet_type, src_port, dest_port, ack_no, seq_no, data)
    return packet

'''
Copies the file name and its data to the specified directory.

:param conn: This is the connection setup to receive the sent data.
:param directory: This is the directory in which the file is needed to be created.
:param clientIP: This is the IP of the client machine.
'''
def sendAck(conn):
    pkt_data = "received packet"
    while True:
        packet = conn.recv(SIZE).decode(FORMAT)
        data = packet.data
        ack = packet.ack_no
        seq = packet.seq_no
        
        print("DATA RECIEVED:" + data)
        
        pkt = makePacket(pkt_data, ack+1, seq)
        
        conn.send(pkt)


'''
This is main of the program.
Parses the command line arguements and creates a socket to start the server.
:raise KeyboardInterrupted: Shuts the server down.
:raise Exception: Shuts the server down.
'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=PORT, dest='PORT')
    args = parser.parse_args()
    

    IP = getIP()    
    ADDR = (IP, args.PORT if (args.PORT) else PORT)

    print(f'Starting Server on {ADDR}')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)

    interrupted = False
    try:
        while not interrupted:
            conn, addr = server.accept()
            cIP = addr[0]
            sendAck(conn)
    except KeyboardInterrupt as keyError:
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted
    except Exception as e:
        print(f'\nAn Exception Occured. Shutting Server - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
