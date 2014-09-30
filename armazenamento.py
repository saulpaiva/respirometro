#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Controlador da estação biométrica
# 
# Centro de Tecnologia Acadêmica - UFRGS
# http://cta.if.ufrgs.br
#
# Licença: GPL v3

#Ordem de parametros : [porta],[banda],[nome_arquivo],[frequencia]
#Exemplo: armazenamento '/dev/ttyACM0' 115200 teste1 5
import sys, time, serial, datetime
parametro = sys.argv[1:]

#Iniciando comunicação serial
ser = serial.Serial(parametro[0], parametro[1])
time.sleep(2)

#Arquivos de log
fisiologfile = open(parametro[2]+'.log','w')
now=datetime.datetime.now()
fisiologfile.write(now.strftime("#Estação Biométrica\n"+"#Frequência de operação "+parametro[3]+"\n"+"#Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"))

frequencia = parametro[3]
periodo = 1.0/int(frequencia)
while True:
	t0 = time.time()
	try:
    		# Temperatura
    		t = float(ser.readline().replace('\r\n',''))
  	except KeyboardInterrupt:
    		break
	except ValueError:
		print "Não é possível operar a essa frequência (controlador)"
		break	

	try:
		# Registra horário atual
		now = datetime.datetime.now()
 
		# Arquivo de log
		print now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],"\t", t,"\t"
		fisiologfile.write(now.strftime("%Y%m%d%H%M%S%f")[:-3]+"\t"+str(t)+"\n")   
		if (periodo - (time.time()- t0))< 0:
			print "Não é possível operar a essa frequência"
			break 		
		time.sleep(periodo - (time.time()- t0))
	except KeyboardInterrupt:
    		break
ser.close()
