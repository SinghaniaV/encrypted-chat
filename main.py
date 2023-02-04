import socket
import threading

# for asymmetric encryption
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Do you want to host (1) or to connect (2): ")

## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)

print(f" your IP address: {ip_address}")

if choice == "1":
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((ip_address, 9999))
	server.listen()
    
	client, client_address = server.accept()
	print(f" user with IP address: {client_address[0]} has connected")
	client.send(public_key.save_pkcs1("PEM"))
	public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((ip_address, 9999))
	public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
	client.send(public_key.save_pkcs1("PEM"))

else:
	exit()

def sending_messages(c):
	while(True):
		message = input("")
		c.send(rsa.encrypt(message.encode(), public_partner))
		print("You: " + message)

def receiving_messages(c):
	while(True):
		print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())

threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
