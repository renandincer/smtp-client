# RENAN DINCER
# A SUPER SIMPLE COMMAND LINE SMTP CLIENT
# NO ENCRIPTION OR FANCYNESS LIKE THAT

from socket import *

# ask for server name
server_name = raw_input('SMTP Server Name:')
server_port = 25

# ask for from address
from_address = raw_input('Your email: ')

# ask for from real name
from_real = raw_input('Your real name: ')

# ask for to adresses
to_addresses = raw_input('Email to (seperate with commas):')
to_list = [x.strip() for x in to_addresses.split(',')] #cleanup

# ask for subject
subject = raw_input('Enter subject:')

# ask for message
message = raw_input('Enter your message:')

# communicate with the server
try:
	# establish sockets
	email_socket = socket(AF_INET, SOCK_STREAM)
	email_socket.connect((server_name,server_port))

	# should get connection response
	server_response = email_socket.recv(4096)
	if server_response.startswith('220'):
		print('connected to server')
	else:
		raise Exception("unexpected response")

	# send HELO
	email_socket.send("HELO " + server_name + "\r\n")
	server_response = email_socket.recv(4096)

	# send MAIL from:
	email_socket.send("MAIL from:<" + from_address + ">"  + "\r\n")
	server_response = email_socket.recv(4096)

	# for all receiptients send RCPT to:
	for address in to_list:
		email_socket.send("RCPT to:<" + address + ">" + "\r\n")
		server_response = email_socket.recv(4096)

	# send DATA
	email_socket.send("DATA" + "\r\n")

	# from header in DATA (also shows real name in paranteses)
	email_socket.send("from:" + from_address + "(" + from_real + ")" + "\r\n")

	# header for to's in DATA
	adresses_comma_sepatated = ""
	for address in to_list:
		adresses_comma_sepatated = adresses_comma_sepatated + address + ","
	adresses_comma_sepatated = adresses_comma_sepatated[:-1]
	email_socket.send("to:" + adresses_comma_sepatated + "\r\n")

	# header for subject in DATA
	email_socket.send("subject:" + subject + "\r\n")

	# message in DATA
	email_socket.send(message + "\r\n")

	# dot ending DATA
	email_socket.send("." + "\r\n")

	server_response = email_socket.recv(4096)
	server_response = email_socket.recv(4096)

	# check got it
	if server_response.startswith('250'):
		print('message sent!')
	else:
		print('the message could not be sent.')
		print(server_response)
except:
	print("the message could not be sent.")
finally:

	#close socket at the end of everything.
	email_socket.close()
