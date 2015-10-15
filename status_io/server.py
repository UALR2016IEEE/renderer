import multiprocessing
import multiprocessing.connection
from threading import Thread


class IOHandler(multiprocessing.Process):
    def __init__(self):
        self.halt = multiprocessing.Value('b', False)
        self.data = multiprocessing.Queue()
        multiprocessing.Process.__init__(self, target=self.io_inf, args=(self.data, self.halt))

    def start(self):
        self.halt.value = False
        super(multiprocessing.Process, self).start()

    def stop(self):
        self.halt.value = True

    def send_data(self, item):
        self.data.put(item)

    def handle_client(self, client):
        while True:
            print('waiting for client data')
            try:
                data = client.recv()
                print("data", data)
            except ConnectionError:
                print("connection error with client, closed")
                break

    def io_inf(self, q, halt):
        host, port = 'localhost', 9999
        server = multiprocessing.connection.Listener((host, port))
        print('server running')
        while not halt.value:
            print('waiting for client connection')
            client = server.accept()
            print('client connected')
            t = Thread(target=self.handle_client, args=(client, ))
            t.daemon = True
            t.start()
