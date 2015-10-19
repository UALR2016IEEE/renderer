import multiprocessing
import multiprocessing.connection
from threading import Thread


class IOHandler(multiprocessing.Process):
    def __init__(self):
        self._halt = multiprocessing.Value('b', False)
        self.outgoing = multiprocessing.Queue()
        self.incoming = multiprocessing.Queue()
        multiprocessing.Process.__init__(self, target=self.io_inf, args=(self.incoming, self.outgoing, self.halt))

    @property
    def halt(self):
        return self._halt.value

    @halt.setter
    def halt(self, value):
        self._halt.value = value

    def start(self):
        self.halt = False
        super(multiprocessing.Process, self).start()

    def stop(self):
        self.halt = True

    def send_data(self, item):
        self.outgoing.put(item)

    def handle_client(self, client, halt, incoming, outgoing):
        while not halt:
            if client.poll(0.1):
                try:
                    data = client.recv()
                    incoming.put(data)
                except ConnectionError:
                    print("connection error with client, closed")
                    break
        client.close()

    def io_inf(self, incoming, outgoing, halt):
        host, port = 'localhost', 9998
        server = multiprocessing.connection.Listener((host, port))
        print('server running')
        while not halt:
            print('waiting for client connection')
            client = server.accept()
            print('client connected')
            t = Thread(target=self.handle_client, args=(client, halt, incoming, outgoing))
            t.daemon = True
            t.start()
