import Packet
import socket
import socket
import argparse
import time

PORT = 5000
FORMAT = 'utf-8'
SIZE = 4096
MSS = 1024

def getData(data, frm, to):
    return data[frm:to]

def makePacket(data, ackN, seqN) -> Packet:
    packet_type = 'data'
    src_port = 5000
    dest_port = 5000
    ack_no = ackN
    seq_no = seqN
    data = data
    packet = Packet(packet_type, src_port, dest_port, ack_no, seq_no, data)
    return packet

def waitForEvent():
    time.sleep(5)
    #  if timer timeout and reaches here and 
    # if dont have any ack then we resend the same pkt else send next packet

def sendData(client, data) -> None:
    
    ack = 0
    seq = 0
    frm = 0
    to = 1023
    
    canSend = True
    sendPacket = True
    recvAck = False
    if sendPacket and canSend: 
        # GET DATA
        pkt_data = getData(data, frm, to)

        # MAKE PACKET
        pkt = makePacket(pkt_data, ack, seq)

        # SEND PACKET 
        client.send(pkt)
        canSend = False
        recvAck = True
        

    # need to calculate how much is an idea time to wait for the ack and use it
    
    waitForEvent()

    if not canSend and recvAck:
        response = client.rec(SIZE).decode(FORMAT)
        if response.ack_no == ack + 1 and response.seq_no == seq:
            canSend = True

    client.close()
        

def main() -> None:    
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, dest='IP', required=True)
    parser.add_argument('-p', type=int, default=PORT, dest='PORT')
    args = parser.parse_args()

    ADDR = (args.IP , args.PORT if (args.PORT) else PORT)
    interrupted = False
    try:
        print(f'Starting Client on {ADDR}')

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        data = input('enter file name or string\n')

        sendData(client, data)
            
    except KeyboardInterrupt as keyError:
        print(f'\nShutting Server - {repr(keyError)}')
        assert not interrupted
    except Exception as e:
        print(f'\nAn Exception Occured. Shutting Client - {repr(e)}')
        assert not interrupted


if __name__ == '__main__':
    main()
