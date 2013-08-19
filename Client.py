# Echo client program
import socket
import time

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start():
	try:
		s.connect((HOST, PORT))
	except:
		Redo()
	print''
	print'Connected!'
	main()

def main():
	ask = raw_input()
	s.send(ask)
	data = s.recv(1024)
	print 'Received', repr(data)
	main()
	
def Redo():
	print"There is no connection"
	time.sleep(1)
	print"Try Again? (y/n)"
	answer = raw_input()
	if answer in('y', 'Y'):
		main()
	if answer in('n', 'N'):
		print"Goodbye"
		time.sleep(1)

start()