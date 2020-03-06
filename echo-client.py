#!/usr/bin/env python3

# el mismo cliente se ejecuta en diferentes procesos a la vez para simular diferentes

import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 6543  # The port used by the server
buffer_size = 1024


try:
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")

    msj = "test"
    TCPClientSocket.sendall(msj.encode())
    print ("Esperadno respuesta")
    data = TCPClientSocket.recv(buffer_size)
    print ("Recibido", repr(data), " de", TCPClientSocket.getpeername())

    TCPClientSocket.close()
except:
    print ("errror")