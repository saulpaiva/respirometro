#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#Ordem de parametros : [porta],[banda],[nome_arquivo],[frequencia]
import sys, time, serial, datetime
parametro = sys.argv[1:]

#Ver paramentros, TIRAR DEPOIS
print parametro

#Iniciando comunicação serial
ser = serial.Serial(parametro[0], parametro[1])
#ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)

#Arquivos de log
fisiologfile = open(parametro[2]+'.log','w')
now=datetime.datetime.now()
fisiologfile.write(now.strftime("Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"))

frequencia = parametro[3]
periodo = 1.0/frequencia
while True:
	t0 = time.time()
	try:
    		# Temperatura
    		t = float(ser.readline().replace('\r\n',''))
  	except KeyboardInterrupt:
    		break
	try:
		# Registra horário atual
		now = datetime.datetime.now()
 
		# Arquivo de log
		print now.strftime("%Y%m%d%H%M%S"),"\t", t,"\t"
		fisiologfile.write(now.strftime("%Y%m%d%H%M%S")+"\t"+str(t)+"\n")   
		if (periodo - (time.time()- t0))< 0:
			print "Não é possível operar a essa frequência"
			break 		
		time.sleep(periodo - (time.time()- t0))
	except KeyboardInterrupt:
    		break
ser.close()
