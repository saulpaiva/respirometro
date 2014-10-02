#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import *
import time, serial, datetime

#Iniciando comunicação serial
ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)

#Arquivos de log
fisiologfile = open('fisiolog.log','w')
now=datetime.datetime.now()
fisiologfile.write(now.strftime("Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"))

frequencia =  5
periodo = 1.0/frequencia

ti=time.time()
flag = 0 
while True:
	t0 =time.time()
	try:
    		# Temperatura
    		ser.write('t')
    		t = float(ser.readline().replace('\r\n',''))
  	except KeyboardInterrupt:
    		break
	try: 
		if (periodo - (time.time()-t0))< 0 and flag == 1:
			print "Não é possível operar a essa frequência"
			break
		#Para estudo de variações:
		fisiologfile.write(str(time.time() - ti)+"\t"+str((time.time()- t0)*1000)+"\n") 		
		print " tempo gasto ",time.time()- t0, " sleep ", periodo - (time.time()-t0)
		if flag == 1: 		
			time.sleep(periodo - (time.time()-t0))
		flag = 1
	except KeyboardInterrupt:
    		break

ser.close()
