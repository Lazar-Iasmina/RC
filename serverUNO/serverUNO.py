import echo_util
import threading
import socket
import sys

HOST = echo_util.HOST
PORT = echo_util.PORT
lista=[]
ok=0
mesaj1=""
def read(sock):
    global mesaj1
    while True:
        m = echo_util.recv_msg(sock)  # Blocks until received
        mesaj1=m
        print(m)
def handle_client(sock, addr):
    """ Receive data from the client via sock and echo it back """
    global mesaj1
    while True:
        try:

            mesaj=mesaj1
            ok=1
            #print("mesaj inside "+ mesaj+ "   "+ mesaj1)
            if mesaj != "":
                print("mesaj inside " + mesaj + "   " + mesaj1)
                for i in range(len(lista)):
                    echo_util.send_msg(lista[i], mesaj)
                #echo_util.send_msg(sock, msg)
                # complete message
                print('{}: {}'.format(addr, mesaj))
                mesaj1=""

        except (ConnectionError, BrokenPipeError):
            print('Closed connection to {}'.format(addr))
            sock.close()
            break


if __name__ == '__main__':
    listen_sock = echo_util.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))



    while True:
        client_sock, addr = listen_sock.accept()
        infolist = socket.getaddrinfo(
            HOST, PORT, 0, socket.SOCK_STREAM, 0,
            socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME,
        )
        print(addr)
        #lista.append(infolist[0])
        echo_util.send_msg(client_sock,"0")
        lista.append(client_sock)
        #a=echo_util.recv_msg(client_sock)
        #b=echo_util.recv_msg(client_sock)
        #l=[a,b]
        #lista.append(l)
        # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
        thread = threading.Thread(target = handle_client, args = [client_sock, addr], daemon=True)
        thread.start()
        thread1 = threading.Thread(target=read, args=[client_sock], daemon=True)
        thread1.start()
        print('Connection from {}'.format(addr))