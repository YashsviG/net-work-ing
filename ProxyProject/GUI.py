from matplotlib import pyplot as plt
import numpy


def format_data(dropped_packets):
    array = []
    total = len(dropped_packets)
    array.append(total)
    for dropped in dropped_packets:
        array.append(total - dropped)
        total -= dropped
    return array


def main():
    timestamps = numpy.arange(10)
    print(timestamps)

    test_data = [0, 0, 1, 0, 0, 1, 0, 1, 1]
    data = format_data(test_data)
    print(data)

    test_acks = [0, 1, 0, 1, 1, 0, 1, 0, 1]
    acks = format_data(test_acks)
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

if __name__ == '__main__':
    main()

