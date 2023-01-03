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