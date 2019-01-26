# -*- coding: UTF-8 -*-

from Crypto.Cipher import AES
from Crypto import Random

iv = Random.new().read(AES.block_size)

def encrypt(text, key, inicialization_vector=iv):
		
	ces = AES.new(key, AES.MODE_CFB, inicialization_vector)
	cipher_end = inicialization_vector + ces.encrypt(text)
	return cipher_end.encode("hex")
	
def decrypt(text, key, inicialization_vector=iv):

	ces = AES.new(key, AES.MODE_CFB, inicialization_vector)
	return ces.decrypt(text.decode("hex"))[AES.block_size:]