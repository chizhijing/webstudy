import socket
import unittest

class SocketMt5Base:
    def __init__(self, address='127.0.0.1', port=9090):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.sock.bind((self.address, self.port))
        self.cummdata = ''

    def recvmsg(self, m): # 发送账户号信息，并等待接收对应账户的交易记录
        pass

    def __del__(self):
        self.sock.close()

class SocketDealRecord(SocketMt5Base):
    def __init__(self,address='127.0.0.1',port=9090):
        SocketMt5Base.__init__(self,address=address,port=port)
        self.cummdata=''

    def recvmsg(self, m):
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        self.cummdata = ''
        conn.send(m)
        while True:
            data = conn.recv(10000)
            rec = data.decode("utf-8")
            self.cummdata += rec
            if not data:
                self.sock.close()
                return self.cummdata

    def close(self):
        self.sock.close()

class SocketDealRecordTestCase(unittest.TestCase):
    def setUp(self):
        self.socket_server=SocketDealRecord()

    def tearDown(self):
        #print('test')
        #self.socket_server.__del__()
        self.socket_server.close()

    def test_recvmsg(self):
        msg=self.socket_server.recvmsg(bytes('50318232', "utf-8"))
        print(msg)

if __name__=='__main__':
    unittest.main()