# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)

def main():
	conn, addr = s.accept()
	print 'Connected by', addr
	while 1:
		con1 = Connect(addr)
		con1.displayCount()
		data = conn.recv(1024)
		eval(data)
		main()
	while 2:
		con2 = Connect(addr)
		con2.displayCount()
		data = conn.recv(1024)
		eval(data)
		main()
	if 0:
		main()

def test():
	x = 5
	conn.send(x)
	main()

class Connect:
	'Client Connections and assigning'
	clientCount = 0
	
	def __init__(self, address):
		self.address = address
		Connect.clientCount += 1
		self.client = Connect.clientCount
		
	def displayCount(self):
		print "Total number of clients connected %d" % Connect.clientCount

	def displayClient(self):
		print "Client : ", self.client, "  Address : ", self.address
		

main()
		
conn.close()