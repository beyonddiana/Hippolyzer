import socket

from zope.interface import implements

from pyogp.lib.base.network.interfaces import IUDPClient
from pyogp.lib.base.message.circuitdata import Host

#returns true if packet was sent successfully
class NetUDPClient(object):
    implements(IUDPClient)

    def __init__(self):
        self.sender = None

    def get_sender(self):
        return Host(self.sender.host, self.sender.port)
    
    def send_packet(self, sock, send_buffer, host):
        print 'Sending to: ' + str(host.ip) + ":" + str(host.port)
        bytes = sock.sendto(send_buffer, (host.ip, host.port))
    
    def receive_packet(self, sock):
        buf = 10000
        data, addr = sock.recvfrom(buf)
        self.sender.ip_addr = addr
        self.sender.port()
        return data, len(data)

    def start_udp_connection(self, port):
        """ Starts a udp connection, returning socket and port. """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        #error check - make sure sock is good

        #will probably be other setup for this
        return sock
