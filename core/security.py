# -*- coding: UTF-8

from crypter import encrypt, decrypt

class passwordLimit(Exception): pass

class repeatLimit(Exception): pass

class Secure:

	def __init__(self, password, repeat=1):
		
		if (int(len(password)) <> 32):
		
			raise passwordLimit("La contrasena debe tener una logitud de 32 caracteres.")
		
		if (int(repeat) < 1):
			
			raise repeatLimit("Las repeticiones deben ser minimo de 1.")
		
		self.password = password
		self.repeat = repeat
		
	def encrypt(self, string):
	
		string = str(string)
	
		for i in range(self.repeat):
	
			string_toencrypt = encrypt(string, self.password)
			
			string = string_toencrypt
		
		return string
		
	def decrypt(self, string):
	
		for i in range(self.repeat):
	
			string_todecrypt = decrypt(string, self.password)
			
			string = string_todecrypt
	
		return string