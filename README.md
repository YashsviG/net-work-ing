# Lossy Network Simulation

## Introduction and Purpose
We achieve lossy network program by implementing a Send-And-Wait protocol. The program simulates a network of varying reliability between the two hosts, i.e., the sender and the receiver. The proxy allows us to control “noise” which in turn increases or decreases the drop/delay rate of the DATA or ACK packets between the hosts.

## Implemented
- Proxy can take the user’s input for drop rate and delay rate for Data and Ack packets through config.json
- Sender re-transmits the same data packet for which the ACK isn’t received
- Receiver can detect duplicate and re-sends the ack packet
- GUI graphs the data for Sender, Proxy, and the Receiver hosts

## Language 
- Python 3

## Screenshots
  <img width="889" alt="Screen Shot 2023-01-03 at 12 09 47 PM" src="https://user-images.githubusercontent.com/45160510/210310298-9b0da9e8-c488-425e-9b65-044eb9a70449.png">
<img width="889" alt="Screen Shot 2023-01-03 at 12 10 53 PM" src="https://user-images.githubusercontent.com/45160510/210310409-d8463d96-3dca-4403-8ec5-32e01c8e1a41.png">
