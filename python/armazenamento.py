#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Estação biométrica CTA
#
# Programa para aquisição dos dados
# Este programa é utilizado com o programa biometrica.ino no qual a taxa de amostragem é definida no microcontrolador
#
# Protocolo usado está disponível no biométrica.ino
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
ser.setDTR(True)  # Liga DTR novamente 

# Variáveis de controle
frequencia = int(ser.readline().replace('\r\n',''))

# Arquivos de log
fisiologfile = open(argumento[2],'w')
now=datetime.datetime.now()
fisiologfile.write(now.strftime("#Frequência\t"+str(frequencia)+"\n"+"#Estação Biométrica\n"+"#Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"+"#Protocolo usado: a primeira coluna é a medida do primeiro termistor e a segunda do segundo.\n"))
fisiologfile.close()
while 1:
	try:
		option = ser.read()
		# Respiração
		# 	Para o python '\x' serve para representar uma caracter HEX ASCII
		# 	e o 0x para para valores HEX literais. O comando write do arduino
		#	  envia um caracter, logo deve-se usar a primeira forma
		if option == '\x0A': 

			sensor_value1 = ser.readline().replace('\r\n','')
			sensor_value2 = ser.readline().replace('\r\n','')

			# Arquivo de log
			fisiologfile = open(argumento[2],'a')
			fisiologfile.write(str(sensor_value1)+"\t"+str(sensor_value2)+"\n")   
			fisiologfile.close()
		
			# Registra horário atual
			now = datetime.datetime.now()
				
			# Mostrando dados na tela
			print now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],"\t", sensor_value1, "\t", sensor_value2

		# Erro 1
		if option == '\x01':
			print 'Frequência muito alta para o microcontrolador: ', frequencia, '. Finalizando processo.\n' 

		
	
	except KeyboardInterrupt:
				break
				
ser.close()
