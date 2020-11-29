import socket
import pickle
from cryptosystem.decryption import decrypt

# creating the socket
socket = socket.socket()
print('Socket successfully created.')

# binding the socket to a particular IP and Port
host = '127.0.0.1'
port = 17041
socket.bind((host, port))
print(f"Socket binded to {port}")

# server is listening for client request
socket.listen(5)
print('Socket is listening')

while True:
	# server accepts client request
	c, addr = socket.accept()
	# server receives the data sent by client
	data = c.recv(1024)
	data = pickle.loads(data)
	# extracting the cipher and key matrix for decryption
	cipher = data[0]
	keyMatrix = data[1]
	print(f"\nReceived encrypted message from the client: {cipher}")
	# decrypting the cipher
	decryptedText = decrypt(cipher, keyMatrix)
	decryptedText = decryptedText.replace('#', '').lower()
	print(f'Actual message sent by the client: {decryptedText}')

# closing the connection
c.close()