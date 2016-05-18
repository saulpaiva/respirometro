# -*- coding: utf-8 -*-
'''
 Respirômetro - Fisiolog CTA

 Programa para aquisição dos dados
 Este programa é utilizado com o programa respirometro.ino no

 Protocolo usado:
    Primeiro número recebido é a frequência de operação do equipamento.
    Demais números são relativos a leituras realizadas pelo microcontrolador

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

STRUCT_DATA = 'hhh'
STRUCT_HEADER = 'Hh'

# Exemplo: python storeBinData.py /dev/ttyACM0 115200 coleta_Nome_Exemplo_1min.log 30

import sys, serial, datetime, os, time, struct

def validateInput():
    '''
        Verificando se os inputs estão corretos.
    '''
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
    ser.dtr = False # Desliga DTR 
    time.sleep(1)
    ser.reset_input_buffer()	# Limpa buffer de dados
    ser.dtr = True  # Liga DTR novamente
    return ser

def progressBar(percent, lenght):
    '''
        Cursor necessita estar na linha onde está a barra de progresso.
        DOC dos ANSII caracters:
            http://ascii-table.com/ansi-escape-sequences.php
    '''
    highlight = " "*int((lenght-2)*percent*1.0/100)
    notHighlight = " "*(lenght-2- len(highlight))
    printString = "\t"+"\033[47m"+" "+"\033[42m"+"{}".format(highlight)+ \
                    "\033[0;0m"+"{}".format(notHighlight)+ "\033[47m"+" "\
                    "\033[0;32m"+"\t{}%".format(percent)+"\033[0;0m" 
    print(printString, end='\r') 

def main(args):
    
    while True:
        try:
            comm = initSerial(args['SerialPort'], args['BaudRate'])
            # Recebendo HEADER de controle
            print("Lendo cabeçalho de controle...")
            dataLen = int(struct.unpack('B', comm.read(1))[0])
            rawData = comm.read(dataLen)    
            flagControl, freq = struct.unpack(STRUCT_HEADER, rawData)
            # Protocolo de comunicação usado envia os bytes 0xAA e 0xAA para 
            #   indicar que o HEADER está sendo enviado
            if flagControl == 0xAAAA: 
                break
            print("Leitura falhou. Reiniciando.")
        except KeyboardInterrupt:
            sys.exit()
        except struct.error:
            print("Leitura falhou. Reiniciando.")
        
    print("Frequência de operação é de {} Hz.".format(freq))
    scriptTime = int(freq*args['ExecTime'])

    dataFile = open(args['FileName'],'w')
    dataFileBin = open(args['FileName']+'bin','wb')

    dataFile.write("# ----CTA||IF||UFRGS---- RESPIRÔMETRO LOGGER\n")
    dataFile.write("# Frequencia de operação: "+str(freq)+"\n")
    dataFileBin.write(struct.pack('h',freq)) 
    # Registra horário atual
    now = datetime.datetime.now()
    dataFile.write("# Data do início da coleta: " + \
            now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]+"\n")
    dataFile.write("# Tempo estimado de coleta: {}s\n".format(args['ExecTime'])) 
    dataFile.write("# A0\tA1\tA5\tTempo(s)\n")
    timeCounter = 0
    print("Iniciando aquisição de dados.")
    while (timeCounter <= scriptTime or scriptTime == 0):
        timeCounter += 1
        if not(timeCounter % int(scriptTime/100)):
           progressBar(int(timeCounter*1.0/scriptTime*100), 40)
        try:
            dataLen = int(struct.unpack('B', comm.read(1))[0])
            rawData =  comm.read(dataLen)
            data = struct.unpack(STRUCT_DATA, rawData)
            # Arquivo de log
            dataFile = open(args['FileName'],'a')
            dataFileBin = open(args['FileName']+'bin','ab')
            for i in range(0, len(data)):
                dataFile.write(str(data[i])+"\t")
            dataFile.write(str(timeCounter/scriptTime*args['ExecTime'])+"\n")
            dataFileBin.write(rawData)
            dataFile.close()
            dataFileBin.close()

        except KeyboardInterrupt:
            print("\nTecla de escape prescionada. Abortando")
            sys.exit()
        except serial.serialutil.SerialException:
            print("\nComunicação serial foi interrompida. Abortando")
            sys.exit()
        

    comm.close()
    print("\nOperação finalizada com sucesso.")
    
if __name__== '__main__':
    args = validateInput()
    main(args)
