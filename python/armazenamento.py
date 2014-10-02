#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Estação biométrica CTA
#
# Programa para aquisição dos dados
# Este programa é utilizado com o programa biometrica.ino no qual a taxa de amostragem é definida no microcontrolador
# 
# Centro de Tecnologia Acadêmica - UFRGS
# http://cta.if.ufrgs.br
#
# Licença: GPL v3
# Ordem de argumentos : [porta],[taxa_transmissão],[arquivo_saída],[frequência]
# Onde 
# [porta]: porta serial no qual o arduino está conectado
# [taxa_transmissão]: velocidade de comunicação serial
# [arquivo_saída]: nome do arquivo em que os dados serão salvos
# [frequência]: frequência de coleta de dados definida no arduino

# Exemplo: python armazenamento.py '/dev/ttyACM0' 115200 coleta1.log 5



import sys, time, serial, datetime
argumento = sys.argv[1:] #renomeando os argumentos 

#Iniciando comunicação serial
ser = serial.Serial(argumento[0], argumento[1])
time.sleep(2)

#Arquivos de log
fisiologfile = open(argumento[2],'w')
now=datetime.datetime.now()
fisiologfile.write(now.strftime("#Frequência\t"+argumento[3]+"\n"+"#Estação Biométrica\n"+"#Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"))

#Variáveis de controle
frequencia = argumento[3]
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
		fisiologfile = open(argumento[2],'a')
		fisiologfile.write(str(t)+"\n")   
		fisiologfile.close()
		if (periodo - (time.time()- t0))< 0:
			print "Não é possível operar a essa frequência"
			break 		
		time.sleep(periodo - (time.time()- t0))
	except KeyboardInterrupt:
    		break
ser.close()
