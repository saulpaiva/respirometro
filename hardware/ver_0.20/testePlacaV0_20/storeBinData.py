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
STRUCT_DATA = 'hhf'
STRUCT_HEADER = 'h'
# Exemplo: python armazenamento_new.py /dev/ttyACM0 115200 coleta_Nome_Exemplo_1min.log 30

import sys, serial, datetime, os, time, struct


def validateInput():
    argumento = sys.argv[1:] #renomeando os argumentos
    baudRate = [300, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
   
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

    if not int(argumento[1]) in baudRate:
        sys.stderr.write('ERRO: A taxa de transmissão '+argumento[1]+' não pode ser usada pelo microcontrolador!\nEm caso de dúvidas leia o READ_ME.md.\n')
        sys.exit(1)

    return {'SerialPort':argumento[0], 'BaudRate':int(argumento[1]), 'FileName':argumento[2], 'ExecTime':int(argumento[3])}

def initSerial(port, baud):
    # Iniciando comunicação serial
    ser = serial.Serial(port, baud)
    # Limpando buffer para retirar as medidas feitas antes de iniciar o software
    ser.setDTR(False)	# Desliga DTR
    time.sleep(0.05)
    ser.flushInput()	# Limpa buffer de dados
    ser.setDTR(True)  # Liga DTR novamente
    return ser

def main():
    
    args = validateInput()
    serial = initSerial(args['SerialPort'], args['BaudRate'])
    freq = int(struct.unpack('h', serial.read(2))[0])
    scriptTime = int(freq*args['ExecTime'])

    timeCounter = 0
    while (timeCounter <= scriptTime or scriptTime == 0):
        timeCounter += 1
        try:
            dataLen = int(struct.unpack('B',serial.read(1))[0])
            rawData =  serial.read(dataLen)
            data = struct.unpack(STRUCT_DATA, rawData)
            # Arquivo de log
            dataFile = open(args['FileName'],'a')
            dataFileBin = open(args['FileName']+'bin','ab')
            dataFile.write(str(data[0])+"\t"+str(data[1])+"\t"+str(data[2])+"\n")
            dataFileBin.write(rawData)
            dataFile.close()
            dataFileBin.close()

        except KeyboardInterrupt:
            break

    serial.close()    

if __name__== '__main__':
    main()
