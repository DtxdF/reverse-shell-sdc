# -*- coding: UTF-8 -*-
# SDC - Secure Data Connection Module. https://github.com/DtxdF/sdc
#
# Hola, Soy DtxdF (Jesus Daniel Colmenares Oviedo), les vengo a traer un modulo facil de
# Usar para que la conexion de sus datos sean seguros, sin ninguna intervencion de algun
# Tercero o software de seguridad. Lo llamo: "Secure Data Connection" - (SDC).
# Solo vaya leyendo las lineas que sean interesantes (Todas! :D), para que vaya entiendo
# y pueda ir personalizandolo a su gusto.
#
# Basicamente es un protocolo, ya que para que se puedan comunicar el cliente
# y el servidor es necesario cumplir una serie de reglas.
#

# Aclaracion: No comentare todas la lineas (Mas que todo las tipicas) y debe tener una
# idea clara de que es un socket, para que sirven y como usarlos (Sin importar el lenguaje de programación).

# Nota: Algunos metodo requiren la reconexion de un socket.

import socket
import thread
from json import loads, dumps

# Este modulo es el mas importante, ya que es el encargado de que la conexion de sus datos sea segura. Basicamente envia datos encriptados y cuando se reciben se desencriptan.

from security import Secure

class serverStart(Exception): pass

class clientNotFound(Exception): pass

class corruptData(Exception): pass

class unknownAddr(Exception): pass

class connectError(Exception): pass

def show_error(event, option):

	if (option == 2):
	
		if (event):
			raise serverStart("El servidor ya esta habilitado")
			
	elif (option == 3):
	
		if (event == 0):
	
			raise clientNotFound("No hay suficientes clientes para recibir datos")

corruptdata_message = "Los datos recibidos pueden estar corruptos."
unknownaddr_message = "No se puede envar un dato a esta direccion, porque no existe o no esta conectada"
			
class Connection:

	def __init__(self, host, port, passwd, limit=0, buffer=1000*1000*100, repeat=1):
		
		"""# Explicacion rapida:
		# host: La direccion a la cual conectarse o usar (En el caso del servidor)
		# port: El puerto donde se enviaran o recibir los datos de la conexion
		# passwd: La contrasena que se usara para encriptar y desencriptar los datos
		# limit: El limite de conexiones permitidas en el caso de que se use el servidor
		# buffer: El limite de flujo de datos.
		# repeat: Las repeticiones de encriptacion de un dato. Mientras mas repeticiones mas lento sera el proceso."""
		
		self.host = str(host)
		self.port = int(port)
		self.limit = int(limit)
		self.buffer = int(buffer)
		self.event = socket.socket()
		self.serverSettingsConf = False
		self.crypter = Secure(passwd, repeat)
		self.list = []
		self.start = False
		self.server_data_decrypted = []
		self.client_data_decrypted = []
		
	def client(self):
		
		"""
		Se conecta al socket de la direccion y el puerto que usted especifique.
		"""
		
		self.event = socket.socket()
		
		try:
		
			self.event.connect((self.host, self.port))
		
		except socket.error:
			
			raise connectError("Error conectando al socket en la direccion especificada.")
		
	def client_interact(self, data, client):
	
		"""
		Envia datos hacia un socket que este conectado en el servidor a traves de una direccion especifica.
		"""
	
		encryptedata = self.crypter.encrypt(data)
		length_encrypedata = str(len(encryptedata))
		
		try:
		
			self.client_connection.sendto(length_encrypedata+" "+encryptedata, client)
		
		except socket.gaierror:
		
			raise unknownAddr(unknownaddr_message)
		
	def server_interact(self, data):
	
		"""
		Envia datos hacia el servidor de el socket este conectado.
		"""
		
		encryptedata = self.crypter.encrypt(data)
		length_encrypedata = str(len(encryptedata))
		
		self.event.send(length_encrypedata+" "+encryptedata)
		
	def client_sendfile(self, file, client):
		
		"""
		Envia el contenido de un archivo especificado a traves de un socket en una direccion especifica.
		"""
		
		readfile = open(file, "rb")
		
		self.client_interact(readfile.read(), client)
		
		readfile.close()
		
	def server_sendfile(self, file):
		
		"""
		Envia el contenido de un archivo especificado a traves de un socket hacia el servidor.
		"""
		
		readfile = open(file, "rb")
		
		self.server_interact(readfile.read())
		
		readfile.close()
		
	def client_buffer_interact(self, data, client):
	
		"""
		Este metodo se comunica con el metodo 'client_buffer_recv'.
		Envia datos a un socket con una direccion especifica y los almacena en un buffer con datos relevantes.
		"""
		
		host, port = self.client_connection.getsockname()
		origin = host+":"+str(port)
		encryptedata = self.crypter.encrypt(dumps({"origin":origin, "content":data.encode("hex"), "length":len(data)}))
		length_encrypedata = str(len(encryptedata))
		
		try:
			
			self.client_connection.sendto(length_encrypedata+" "+encryptedata, client)

		except socket.gaierror:
			
			raise unknownAddr(unknownaddr_message)
			
	def server_buffer_interact(self, data):
	
		"""
		Este metodo se comunica con el metodo 'server_buffer_recv'.
		Envia datos a un socket conectado al servidor y los almacena en un buffer con datos relevantes. Este metodo se conecta al socket del servidor cada vez que envia datos.
		"""
		
		self.client()
		
		host, port = self.event.getsockname()
		origin = host+":"+str(port)
		encryptedata = self.crypter.encrypt(dumps({"origin":origin, "content":data.encode("hex"), "length":len(data)}))
		length_encrypedata = str(len(encryptedata))
		
		self.event.send(length_encrypedata+" "+encryptedata)
		
	def server_recv(self):
	
		"""
		Espera el contenido enviado a traves de un socket que este conectado hacia el servidor, para posteriormente retornarlo.
		Este metodo se comunica con el metodo 'server_interact'.
		"""
		
		server_data = ''
		repetir = True

		while True:
		
			try:
					
				data = self.event.recv(self.buffer)
					
				if (repetir):
					
					repetir = False
						
					longitud = int(data.split()[0])
					server_data += data.replace(data.split()[0]+" ", "")
						
				else:
						
					server_data += data
					
				longitud_a_sumar = int(len(server_data))
					
				if (longitud == longitud_a_sumar):
						
					return self.crypter.decrypt(server_data)
		
			except:
				
				raise corruptData(corruptdata_message)
		
	def client_recv(self):
	
		"""
		Espera el contenido enviado a traves de un socket que este conectado hacia un cliente, para posteriormente retornarlo.
		Este metodo se comunica con el metodo 'server_interact'.
		"""
		
		show_error(int(len(self.client_list())), 3)
		show_error(self.serverSettingsConf, 1)
		
		client_data = ''
		repetir = True

		while True:
				
			try:
					
				data = self.client_connection.recv(self.buffer)
					
				if (repetir):
					
					repetir = False
						
					longitud = int(data.split()[0])
					client_data += data.replace(data.split()[0]+" ", "")
						
				else:
						
					client_data += data
					
				longitud_a_sumar = int(len(client_data))
					
				if (longitud == longitud_a_sumar):
						
					return self.crypter.decrypt(client_data)

			except:
				
				raise corruptData(corruptdata_message)
					
	def server_buffer_recv(self, stop=False):
		
		"""
		Recibe los datos que un servidor le envia a un cliente a traves de un socket para almacenarlo en un buffer con datos relevantes y especificos.
		
		El parametro stop: Si el argumento es 'False', no parara de recibir y almacenar datos. Si esta el 'True' cuando reciba un datos de un cliente terminara el bucle.
		
		"""
		
		self.client()
		
		def server_receive():
		
			server_data = ''
			repetir = True

			while True:
			
				try:
					
					data = self.event.recv(self.buffer)
					
					if (repetir):
					
						repetir = False
						
						longitud = int(data.split()[0])
						server_data += data.replace(data.split()[0]+" ", "")
						
					else:
						
						server_data += data
					
					longitud_a_sumar = int(len(server_data))
					
					if (longitud == longitud_a_sumar):
						
						self.server_data_decrypted.append(server_data)
						
						if (stop):
						
							break
							
						else:
							
							server_data = ''
							repetir = True
					
				except:
					
					raise corruptData(corruptdata_message)
					
		output = thread.start_new_thread(server_receive, ())
		
	def server(self, buffer=True):
	
		"""
		Inicia el servidor esperando conexiones.
		
		El parametro buffer: Si el argumento es 'True', recibira datos y los almacenara en un buffer con datos relevantes y especificos. Util a la hora de comunicarse con otros metodos: ej: 'server_buffer_interact'. Si esta en 'False' entonces solo esperara las conexiones.
		"""
		
		show_error(self.start, 2)
		
		def start_with_thread():
		
			self.start = True
			level = 0
			repetir = True
			client_data = ''
			
			self.serverSettingsConf = True
		
			self.event = socket.socket()
			self.event.bind((self.host, self.port))
			self.event.listen(self.limit)
		
			while True:
			
				if (self.limit > 0):
					level += 1
						
				self.client_connection, client = self.event.accept()
				self.list.append(client)
				
				if (buffer):
					
					try:
					
						data = self.client_connection.recv(self.buffer)
						
						if (repetir):
						
							repetir = False
							
							longitud = int(data.split()[0])
							client_data += data.replace(data.split()[0]+" ", "")
							
						else:
							
							client_data += data
						
						longitud_a_sumar = int(len(client_data))
						
						if (longitud == longitud_a_sumar):
						
							self.client_data_decrypted.append(client_data)
							
							client_data = ''
							repetir = True
						
							#if (not self.limit == 0 and level == self.limit):
							#	break
				
					except:
						
						raise corruptData(corruptdata_message)
						
		output = thread.start_new_thread(start_with_thread, ())
		
	def client_list(self):
	
		"""
		retorna la lista de clientes que se han conectado. Nota: No se puede determinar si el cliente ya no esta conectado!.
		"""
	
		return self.list
		
	def server_buffer_print(self):
	
		"""
		Desencripta y descodifica los datos que se almacenan en el buffer que se han enviado a traves del socket del servidor hacia el cliente.
		"""
	
		output = []
	
		for i in self.server_data_decrypted:
			
			output.append(loads(self.crypter.decrypt(i)))
	
		output_decode = []
	
		for i in output:
			
			origin = str(i['origin'])
			content = str(i['content'].decode("hex"))
			length = int(i['length'])
			
			output_decode.append({"origin":origin, "length":length, "content":content})
	
		return output_decode
		
	def client_buffer_print(self):
	
		"""
		Desencripta y descodifica los datos que se almacenan en el buffer que se han enviado a traves del socket del cliente hacia el servidor.
		"""
		
		show_error(self.serverSettingsConf, 1)
	
		output = []
	
		for i in self.client_data_decrypted:
			
			output.append(loads(self.crypter.decrypt(i)))
			
		output_decode = []
	
		for i in output:
			
			origin = str(i['origin'])
			content = str(i['content'].decode("hex"))
			length = int(i['length'])
			
			output_decode.append({"origin":origin, "length":length, "content":content})
	
		return output_decode