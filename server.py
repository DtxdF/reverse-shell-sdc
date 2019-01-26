# -*- coding: UTF-8 -*-

from core.sdc import Connection
from thread import start_new_thread
import sys

# El Host/IP, si quiere que se detecte coloque: "0.0.0.0" o "" (Una cadena vacia)

host = '0.0.0.0'

# El puerto donde recibira la conexion

port = 8443

# La contrasena que debe ser de 32 caracteres

password = "12345678901234567890123456789012"

# Las repeticiones de cifrado y descifrado

repeticiones = 12

conexion = Connection(host, port, password, limit=1, repeat=repeticiones)

# Colocamos 'buffer=False', para que los datos no se almacenen en un buffer y se retornen

conexion.server(buffer=False)

def connection():

	while True:
		
		try:
		
			if (len(conexion.client_list()) > 0):
				
				data = conexion.client_recv()
				
				print "\n\n" + data
		
		except Exception as error:
			
			sys.exit("Exception: %s" % (str(error)))
		
output = start_new_thread(connection, ())
		
print "Esperando conexiones ..."
		
while True:
	
	clients = conexion.client_list()
	
	if (len(clients) > 0):
		
		try:
			
			try:
			
				debug = raw_input("{0}:{1} >>> ".format(*clients[0]))
			
			except KeyboardInterrupt:
				
				break
				
			except EOFError:
				
				continue
			
			if not debug:
				continue
				
			if (debug.split()[0].lower() == 'exit'):
				try:
					conexion.client_interact("exit", clients[0])
				except:
					pass
				break
			else:
				print "Enviando comando a :: {0}:{1} ...".format(*clients[0])
				conexion.client_interact(debug, clients[0])
				
		except Exception as error:
			
			sys.exit("Exception: %s" % (str(error)))