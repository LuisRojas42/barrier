# !/usr/bin/env python3

import socket
import sys
import threading


def servirPorSiempre(socketTcp, listaconexiones, barrier, threads):
    try:
        i = 1
        while len(listaconexiones) != 3:
            client_conn, client_addr = socketTcp.accept()  # recibe conexion
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn) # forma conexion en arreglo
            thread_read = threading.Thread(target=recibir_datos, args=(client_conn, client_addr, barrier), name='worker-%s' % ++i) # crea hilo en recibir_datos de conexion
            threads.append(thread_read)
            thread_read.start() # lanza hilo

            gestion_conexiones(listaConexiones, threads) # actualiza conexiones
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones, threads):
    for conn in listaconexiones:
        if conn.fileno() == -1: # si la conexion actual no existe  remueve de arreglo
            listaconexiones.remove(conn)

    # print("hilos activos:", threading.active_count())
    # print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    # print(listaconexiones) # imprime estado arreglo


def recibir_datos(conn, addr, barrier):
    try:
        cur_thread = threading.current_thread() # auxiliar para hilo actual
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        print(threading.current_thread().name,
              'Esperando en la barrera con {} hilos más'.format(barrier.n_waiting))
        worker_id = barrier.wait()
        while True:
            data = conn.recv(1024) # recibe mensaje
            print("cliente dice ", repr(data))
            # response = bytes("{}: {}".format(cur_thread.name, data), 'ascii') # escribe respuesta
            response = bytes("hi from server", 'ascii')
            if not data:
                print("Fin")
                break
            conn.sendall(response) # envia respuesta
    except Exception as e:
        print(e)
    finally:
        conn.close()



listaConexiones = [] # Arreglo sockets
threads = [] # Arreglo hilos
host, port, numConn = sys.argv[1:4]

NUM_THREADS = numConn
barrier = threading.Barrier(NUM_THREADS)

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port)) # tupla datos conexion

try:
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP esta disponible y en espera de solicitudes")  # Abre y conf

    servirPorSiempre(TCPServerSocket, listaConexiones, barrier, threads) # Socket y arreglo

    for t in threads:  # espera que todos esten listos
        t.join()

    TCPServerSocket.close()
except:
    print ("error")
