#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Estação biométrica CTA
#
# Programa para estudo sobre frequência máxima de operação do armazenamento
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

# Exemplo: python delay_armazenamento.py '/dev/ttyACM0' 115200 delay_arm.log 

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
delay_armazemanto_file = open(argumento[2],'w')
now=datetime.datetime.now()
delay_armazemanto_file.write(now.strftime("#Frequência\t"+str(frequencia)+"\n"+"#Estação Biométrica\n"+"#Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"))

#
contador = 0;
intervalo = frequencia*10
list_time = []

while contador< intervalo:
	try:
    		# Temperatura
    		t0 = time.time()
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
		contador = contador + 1 
		delay_armazemanto_file = open(argumento[2],'a')
		delay_armazemanto_file.write(str(time.time() - t0)+"\n")
		list_time.append(float(time.time() - t0))
		delay_armazemanto_file.close()
	except KeyboardInterrupt:
    		break

frequencia_max = 1.0/(max(list_time)*(1.2))
delay_armazemanto_file = open(argumento[2],'a')
delay_armazemanto_file.write(str(frequencia_max)+"\n")
ser.close()
