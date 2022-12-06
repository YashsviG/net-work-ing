import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import randrange
import numpy

# TODO: 
# 1. Make a graph for the packets received every iteration for receiver
# 2. Make a graph for the packets sent every iteration for sender
# 3. Data Packets dropped or delayed in proxy
# 4. Ack Packets dropped or delayed in proxy

class GUI:
    def __init__(self) -> None:
        ack = []
        data = []
        title = ''
    
    def update_ack(self, data): 
        self.ack.append(data)
    

    def update_data(self, data): 
        self.data.append(data)

    def format_data(self, dropped_packets):
        array = []
        total = len(dropped_packets)
        array.append(total)
        for dropped in dropped_packets:
            array.append(total - dropped)
            total -= dropped
        return array

    def main(self):
        timestamps = numpy.arange(10)
        print(timestamps)
    
        test_data = [0, 0, 1, 0, 0, 1, 0, 1, 1]
        data = self.format_data(test_data)
        print(data)
    
        test_acks = [0, 1, 0, 1, 1, 0, 1, 0, 1]
        acks = self.format_data(test_acks)
        print(acks)    
    
        fig, axs = plt.subplots(2)
        fig.suptitle("Packets Being Dropped")
    
        # plot graphs
        axs[0].step(timestamps, data)
        axs[0].set_title("Data Packets Dropped")
    
        axs[0].set_ylim(0, None)
        axs[0].set_xlim(0, None)
    
        axs[1].step(timestamps, data)
        axs[1].set_title("ACK Packets Dropped")
    
        axs[1].set_ylim(0, None)
        axs[1].set_xlim(0, None)
    
        plt.show()

