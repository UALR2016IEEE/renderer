import multiprocessing
import multiprocessing.connection
from threading import Thread
import select
import socket
import pickle
import struct


class IOHandler(multiprocessing.Process):
    def __init__(self):
        self.halt = multiprocessing.Value('b', False)
        self.outgoing = multiprocessing.Queue()
        self.incoming = multiprocessing.Queue()
        multiprocessing.Process.__init__(self, target=self.io_inf, args=(self.incoming, self.outgoing, self.halt))

    def start(self):
        self.halt.value = False
        super(multiprocessing.Process, self).start()

    def finish(self):
        self.halt.value = True

    def send_data(self, item):
        self.outgoing.put(item)

    def handle_client(self, client, halt, incoming, outgoing):
        while not halt.value:
            try:
                buf = b''

                while len(buf) < 4:
                    buf += client.recv(4 - len(buf))

                length = struct.unpack('!I', buf)[0]
                packet = b''
                while len(packet) < length:
                    packet += client.recv(16777216)

                packet = packet[:length]
                data = pickle.loads(packet)
                incoming.put(data)
            except ConnectionError:
                print("connection error with client, closed")
                break

    def io_inf(self, incoming, outgoing, halt):
        host, port = 'localhost', 9998
        # server = multiprocessing.connection.Listener((host, port))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        print('server running, waiting for client connection')
        while not halt.value:
            r, w, e = select.select([server], [], [], 1)
            print('r', r)
            if len(r) > 0:
                client = server.accept()[0]
                t = Thread(target=self.handle_client, args=(client, halt, incoming, outgoing))
                t.daemon = True
                t.start()
                print('client connected')
        server.close()
