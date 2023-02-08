import socket
import threading

# library for implementing RSA encryption
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Do you want to host (1) or to connect (2): ")

# getting the hostname
hostname = socket.gethostname()
# getting the IP address
ip_address = socket.gethostbyname(hostname)


if choice == "1":
	# using IPv4 and TCP on port choosen by the OS (0)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((ip_address, 0))
	server.listen()

	print(f" Server listening on IP address: {ip_address} and port: {server.getsockname()[1]}")
	
	client, client_address = server.accept()
	print(f" A user with IP address: {client_address[0]} has connected!")

	# sending a welcome message
	client.send(bytes(f"Connected to {ip_address}", "utf-8"))
	# sending our public key to the client
	client.send(public_key.save_pkcs1("PEM"))

	# storing the recieved public key from the client
	public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
	# using IPv4 and TCP
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# getting the IP address of the host client to connect
	server_ip, server_port = input("Please enter the (IP address<space>Port) to which you want to connect: ").split()

	# connecting to IP address and port provided by the client
	client.connect((server_ip, int(server_port)))

	# accepting and printing the recieved message from the server
	print(client.recv(1024).decode("utf-8"));
	# accepting and storing the recieved public key from the server
	public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

	# sending our public key to the server
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
