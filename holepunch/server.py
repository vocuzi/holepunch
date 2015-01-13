import queue
import socket
import threading

import holepunch.config
import holepunch.thread




class Server:

    def __init__(self):
        self._conn = None
        self._addr = (holepunch.config.HOST, holepunch.config.PORT)

        self._rlist = [self._conn]
        self._wlist = []
        self._xlist = []

        self._clients = []

    def open(self):
        print("opening...")
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._conn.bind(self._addr)
        self._conn.listen(5)

    def close(self):
        print("closing...")
        self._conn.shutdown(socket.SHUT_RDWR)
        self._conn.close()

        for client in self._clients:
            client.close()

    def run(self):
        self.open()

        while True:
            try:
                rready, wready, xready = select.select(self._rlist, self._qlist, self._xlist)

                conn, addr = self._conn.accept()

                client = holepunch.client.Client(self._conn, conn, addr)
                self._clients.append(client)
            except KeyboardInterrupt:
                break

        self.close()


class Client:

    def __init__(self, conn, addr):
        self._conn = conn
        self._addr = addr
