# Citation - the following code is adapted from:
#   Author Name(s): The ZeroMQ authors
#   Title of Source: Python
#   Source URL: https://zeromq.org/languages/python/
#   Date Retrieved: 10/23/2022

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
print()

#  Send a message to the server
request = input("Enter the message you would like to send to the server: ")
print("Sending request to server...")
socket.send(request.encode())

#  Get the reply.
print()
print("Received results from server:")
message = socket.recv()
print(message.decode())
