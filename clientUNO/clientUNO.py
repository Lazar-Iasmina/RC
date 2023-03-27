import sys, socket
import echo_util
import threading

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = echo_util.PORT

def sendul(sock,msg):
    while True:
        msg = input()
        if not msg:
            continue
        if msg == 'q': break
        echo_util.send_msg(sock, msg)
        print('Sent message: {}'.format(msg))
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))  #connect to server
        print("here")
    except ConnectionError:
        print('Socket error on connection')
        sys.exit(1)

    print('\nConnected to {}:{}'.format(HOST, PORT))
    msg = echo_util.recv_msg(sock)
    # Block until
    # received complete
    # message
    print('Received echo: ' + msg)
    print("Type message, enter to send, 'q' to quit")

    while True:

        try:
            thread = threading.Thread(target=sendul, args=[sock,msg], daemon=True)
            thread.start()
             # Blocks until sent

            msg = echo_util.recv_msg(sock)
            # Block until
            # received complete
            # message
            print('Received echo: ' + msg)
        except ConnectionError:
            print('Socket error during communication')
            sock.close()
            print('Closed connection to server\n')
            break

    print("Closing connection")
    sock.close()