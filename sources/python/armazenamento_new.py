#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 Estação biométrica CTA

 Programa para aquisição dos dados
 Este programa é utilizado com o programa biometrica.ino no qual a taxa de amostragem é definida no microcontrolador

 Protocolo usado está disponível no biométrica.ino

 Centro de Tecnologia Acadêmica - UFRGS
 http://cta.if.ufrgs.br

 Licença: GPL v3
 Ordem de argumentos : [porta],[taxa_transmissão],[arquivo_saída]
 Onde:
	[porta]: porta serial no qual o arduino está conectado
	[taxa_transmissão]: velocidade de comunicação serial
	[arquivo_saída]: nome do arquivo em que os dados serão salvos
	[tempo_de_execução]: tempo total de execução, em segundos

	PADRÃO NOME DO ARQUIVO DE SAÍDA: coleta_[Nome]_[Sobrenome]_[obs].log
		[obs] são observações caso sejam necessárias
'''
# Exemplo: python armazenamento_new.py /dev/ttyACM0 115200 coleta_Nome_Exemplo_1min.log 30

import sys, serial, datetime, os, time
argumento = sys.argv[1:] #renomeando os argumentos
baud_rate = [300, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
baud_correct = 0

# Erros
if len(sys.argv) < 5:
    sys.stderr.write('ERRO: Argumentos insuficientes.\nEm caso de dúvidas leia o READ_ME.md.\n' )
    sys.exit(1)

if not os.path.exists(argumento[0]):
	sys.stderr.write('ERRO: Arduino não está conectado na porta '+argumento[0]+'!\nEm caso de dúvidas leia o READ_ME.md.\n')
	sys.exit(1)

if not os.access(argumento[0], os.R_OK):
	sys.stderr.write('ERRO: A porta '+argumento[0]+' não pode ser lida por problemas de permissão!\nEm caso de dúvidas leia o READ_ME.md.\n')
	sys.exit(1)

for i in baud_rate:
    if i == int(argumento[1]):
        baud_correct = 1
if not baud_correct:
    sys.stderr.write('ERRO: A taxa de transmissão '+argumento[1]+' não pode ser usada pelo microcontrolador!\nEm caso de dúvidas leia o READ_ME.md.\n')
    sys.exit(1)

# Iniciando comunicação serial
ser = serial.Serial(argumento[0], argumento[1])
# Limpando buffer para retirar as medidas feitas antes de iniciar o software
ser.setDTR(False)	# Desliga DTR
time.sleep(0.05)
ser.flushInput()	# Limpa buffer de dados
ser.setDTR(True)  # Liga DTR novamente

# Variáveis de controle
frequencia = int(ser.readline().replace('\r\n',''))
periodo = 1.0/frequencia
# Arquivos de log
fisiologfile = open(argumento[2],'w')
now = datetime.datetime.now()
fisiologfile.write(now.strftime("#Frequência\t"+str(frequencia)+"\t(Hz)\n"+"#Estação Biométrica\n"+"#Coleta de dados iniciado em: "+"%Y-%m-%d %H:%M:%S" +"\n"+"#Protocolo usado: a primeira coluna é a medida do primeiro termistor e a segunda do segundo.\n"))
fisiologfile.close()

script_time = int(argumento[3])*frequencia
time_counter = 0;

print "Data e hora da medida\t\tMedida 1\tMedida 2"
while (time_counter <= script_time or script_time == 0):
	time_counter += 1
	print str(script_time*periodo) + ' s', str(time_counter*periodo) + ' s'
	try:
		option = ser.read()
		# Respiração
		# 	Para o python '\x' serve para representar uma caracter HEX ASCII
		# 	e o 0x para para valores HEX literais. O comando write do arduino
		#	  envia um caracter, logo deve-se usar a primeira forma
		if option == "\x0A":

			sensor_value1 = ser.readline().replace('\r\n','')
			sensor_value2 = ser.readline().replace('\r\n','')

			# Arquivo de log
			fisiologfile = open(argumento[2],'a')
			fisiologfile.write(str(sensor_value1)+"\t"+str(sensor_value2)+"\n")
			fisiologfile.close()

			# Registra horário atual
			now = datetime.datetime.now()

			# Mostrando dados na tela
			print now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],"\t", sensor_value1, "\t\t", sensor_value2

		# Erro 1
		if option == '\x01':
			print 'Frequência muito alta para o microcontrolador: ', frequencia, '. Finalizando processo.\n'

	except KeyboardInterrupt:
				break

ser.close()
