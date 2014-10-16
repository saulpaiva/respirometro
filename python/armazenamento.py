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
# Ordem de argumentos : [porta],[taxa_transmissão],[arquivo_saída]
# Onde 
# [porta]: porta serial no qual o arduino está conectado
# [taxa_transmissão]: velocidade de comunicação serial
# [arquivo_saída]: nome do arquivo em que os dados serão salvos

# Exemplo: python armazenamento.py '/dev/ttyACM0' 115200 coleta1.log 

import sys, time, serial, datetime
argumento = sys.argv[1:] #renomeando os argumentos 

# Iniciando comunicação serial
ser = serial.Serial(argumento[0], argumento[1])
# Limpando buffer para retirar as medidas feitas antes de iniciar o software
ser.setDTR(False)	# Desliga DTR
time.sleep(0.005)  
ser.flushInput()	# Limpa buffer de dados
ser.setDTR(True)  	# Liga DTR novamente 

# Variáveis de controle
frequencia = int(ser.readline().replace('\r\n',''))
periodo = 1.0/frequencia

# Arquivos de log
fisiologfile = open(argumento[2],'w')
now=datetime.datetime.now()
fisiologfile.write(now.strftime("#Frequência\t"+str(frequencia)+"\n"+"#Estação Biométrica\n"+"#Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"))

while True:
	try:
    		# Temperatura
    		t = ser.readline().replace('\r\n','')
    		if t == 'Erro1':
				print 'Frequência muito alta para o microcontrolador: ', frequencia, '. Finalizando processo.\n' 
  	except KeyboardInterrupt:
    		break
	
	try:
		# Registra horário atual
		now = datetime.datetime.now()
		
		# Mostrando dados na tela
		print now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],"\t", t
 
		# Arquivo de log
		fisiologfile = open(argumento[2],'a')
		fisiologfile.write(str(t)+"\n")   
		fisiologfile.close()
	except KeyboardInterrupt:
    		break
    		
ser.close()
