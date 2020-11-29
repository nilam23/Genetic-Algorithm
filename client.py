import socket
import pickle
from cryptosystem.run import getCipher

socket = socket.socket()

host = '127.0.0.1'
port = 17041
socket.connect((host, port))

msg = input('Enter your message to be sent to the Server: ')
(cipher, keyMatrix) = getCipher(msg)
data = [cipher, keyMatrix]
data = pickle.dumps(data)
socket.send(data)

socket.close()