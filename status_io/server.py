import multiprocessing
import multiprocessing.connection
from threading import Thread


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
                data = client.recv()

                # if data[0] == 'lidar-points':
                #     print(data[0])
                #     print(data[1][0].y, data[1][0].x, data[1][0].r)
                #     for i in range(10):
                #         print(data[1][1][i])
                print('Command Recieved ', data[0])
                incoming.put(data)
            except (ConnectionError, EOFError):
                print("connection error with client, closed")
                break

    def io_inf(self, incoming, outgoing, halt):
        host, port = '', 9998
        server = multiprocessing.connection.Listener((host, port))
        print('server running, waiting for client connection')
        while not halt.value:
            client = server.accept()
            t = Thread(target=self.handle_client, args=(client, halt, incoming, outgoing))
            t.daemon = True
            t.start()
            print('client connected')
        server.close()
