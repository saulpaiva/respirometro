import os, sys

from terminalcolors import colorprint, colorstring
import argparse, subprocess, readchar

# CONSTANTES
LOGPATH = 'logs/'
SOURCEPATH = 'sources/'

shexec = lambda command:\
    subprocess.check_output(command, shell=True).decode('ascii')

def get_plataformio_serial_ports():
    '''

    '''
    serial_raw = shexec("platformio serialports list").splitlines()
    if serial_raw == []:
        # return ['/dev/tty/USB0']
        return []
    else:
        serial_ports = [serial_raw[i-1] 
            for i,x in enumerate(serial_raw) if '----' in x]
    return serial_ports

def serial_ports_menu():
    serials_available = get_plataformio_serial_ports()
    if(serials_available == []):
        print("{} nenhuma porta serial encontrada.\nAbortando.".format(colorstring("ERRO:", attr='bold')))
        sys.exit(0)
    else:
        index = 0
        charac = 0
        while(charac != '\r'):
            print('\r', end = "", flush=True)
            for i, ser in enumerate(serials_available):
                print("{} {} ".format(colorstring("-->", fore='green') if index == i else "   " ,ser), end = "", flush=True)
            charac = readchar.readkey()
            if(charac == '\x1b[C'):
                if(index != len(serials_available) - 1):
                    index += 1
            if(charac == '\x1b[D'):
                if(index != 0):
                    index -= 1
            if(charac == '\x03'):
                print("\nTecla de escape prescionada.\nAbortando")
                sys.exit(1)
        print("")
    return serials_available[index]

def storage_info(inputDic):
    colorprint("Armazenamento:", attr='bold')
    print("-Nome do arquivo: {} \t-Tempo de armazenamento: {} s".format(inputDic['fileName'],inputDic['execTime']))
    print("-Porta Serial: {} \t-Baud Rate: {} ".format(inputDic['serialPort'],inputDic['baudRate']))

def visualization_info(inputDic):
    colorprint("Visualização:", attr='bold')
    print("Tempo:\t\t\tFrequência:\t\t\tFiltro:")
    print("-Inicial: {} s\t\t-Inicial: {} Hz\t\t\t-Ordem: {}".format(inputDic['initialTime'],inputDic['initialFreq'], inputDic['filterOrder']))
    print("-Final: {} s\t\t-Final: {} Hz\t\t\t-Passadas: {}".format(inputDic['finalTime'],inputDic['finalFreq'], inputDic['filterNum']))

def visualization_menu_change_time(inputDic):
    while True:
        try:
            inputDic['initialTime'] = int(input("Insira o tempo inicial de análise: "))
            break
        except ValueError:
            print("Insira um número válido")

    while True:
        try:
            inputDic['finalTime'] = int(input("Insira o tempo final de análise: "))
            break
        except ValueError:
            print("Insira um número válido")
    return inputDic

def visualization_menu_change_freq(inputDic):
    while True:
        try:
            inputDic['initialFreq'] = float(input("Insira a frequência inicial de análise: "))
            break
        except ValueError:
            print("Insira um número válido")

    while True:
        try:
            inputDic['finalFreq'] = float(input("Insira a frequência final de análise: "))
            break
        except ValueError:
            print("Insira um número válido")
    return inputDic

def visualization_menu_change_filter(inputDic):
    while True:
        try:
            inputDic['filterOrder'] = int(input("Insira a ordem do filtro, (MÁX 2): "))
            break
        except ValueError:
            print("Insira um número válido")

    while True:
        try:
            inputDic['filterNum'] = int(input("Insira o número de passadas do filtro: "))
            break
        except ValueError:
            print("Insira um número válido")
    return inputDic

def visualization_menu(inputDic):
    options = ["Não", "Tempo", "Frequência", "Filtro"]
    index = 1
    while(index != 0):
        index = 0
        charac = 0
        print("Deseja modificar algum item ?")
        while(charac != '\r'):
            print('\r', end = "", flush=True)
            for i, ser in enumerate(options):
                print("{} {} ".format(colorstring("-->", fore='green') if index == i else "   " ,ser), end = "", flush=True)
            charac = readchar.readkey()
            if(charac == '\x1b[C'):
                if(index != len(options) - 1):
                    index += 1
            if(charac == '\x1b[D'):
                if(index != 0):
                    index -= 1
            if(charac == '\x03'):
                print("\nTecla de escape prescionada.\nAbortando")
                sys.exit(1)
        print("")
        if(index == 1):
            inputDic = visualization_menu_change_time(inputDic)
        elif(index == 2):
            inputDic = visualization_menu_change_freq(inputDic)
        elif(index == 3):
            inputDic = visualization_menu_change_filter(inputDic)
    return inputDic

def runScripts(inputDic, store=True, analyze=True):
    if not os.access(inputDic['logPath'], os.R_OK):
        os.mkdir(inputDic['logPath'])
    if store and analyze:
        os.system("""
            python3 {srcPath}armazenamento.py {serialPort} {baudRate} \
                    {logPath}{fileName} {execTime} && 
            python3 {srcPath}visualiza.py {logPath}{fileName} {initialTime} \
                    {finalTime} {filterOrder} {filterNum} {initialFreq} {finalFreq}
            """.format(**inputDic))
    elif store:
        os.system("""
            python3 {srcPath}armazenamento.py {serialPort} {baudRate} \
                    {logPath}{fileName} {execTime}
            """.format(**inputDic))
    elif analyze:
        os.system("""
            python3 {srcPath}visualiza.py {logPath}{fileName} {initialTime} \
                    {finalTime} {filterOrder} {filterNum} {initialFreq} {finalFreq}
            """.format(**inputDic))

def checkPath(path):
    a = os.getcwd().split('respirometro')[1]
    return "../"*a.count('/')+path

def main(store=True, analyze=True):
    colorprint("--: Script de coleta e visualização Respirômetro CTA :--", attr='bold', fore='green')
    inputDic = {'initialTime': 0, 'initialFreq': 0, 'finalFreq': 1, 
                'baudRate': 115200, 'filterOrder':2, 'filterNum':4,
                'srcPath':checkPath(SOURCEPATH), 'logPath':checkPath(LOGPATH)}
    if store:
        colorprint("\nArmazenamento:", fore='green')
        inputDic['fileName'] = input("Insira o nome do arquivo em qual será salvo a coleta: ") + '.log'
        print("Selecione a porta usb em que o microcontrolador está conectado.")
        print("Use as teclas direcionais para navegar e enter para selecionar")
        inputDic['serialPort'] = serial_ports_menu()
        while True:
            try:
                inputDic['execTime'] = int(input("Insira o tempo de armazenamento de dados, em segundos: "))
                break
            except ValueError:
                print("Insira um número válido")
    else:
        colorprint("\nVisualização:", fore='green')
        inputDic['fileName'] = input("Insira o nome do arquivo que será analisado: ") + '.log'
        while True:
            try:
                inputDic['execTime'] = int(input("Insira o tempo final de análise, em segundos: "))
                break
            except ValueError:
                print("Insira um número válido")
    if analyze:
        inputDic['finalTime'] = inputDic['execTime']
        colorprint("\nVisualização:", fore='green')
        colorprint("Default:", attr='bold')
        visualization_info(inputDic)
        inputDic = visualization_menu(inputDic)
    colorprint("\nConfirmação:", fore='green')    
    if store and analyze:
        storage_info(inputDic)
        visualization_info(inputDic)
        runScripts(inputDic)
    elif store:
        storage_info(inputDic)
        runScripts(inputDic, store=True, analyze=False)
    else:
        visualization_info(inputDic)
        runScripts(inputDic, store=False, analyze=True)

if __name__ == "__main__":
    #Creating a parser
    parser = argparse.ArgumentParser(description="""Script para realizar 
            armazenamento e visualização dos dados do respirômetro.""")
    parser.add_argument('--store', action='store_true',
            help='Para realizar armazenamento dos dados enviados pela porta serial.')
    parser.add_argument('--analyze', action='store_true',
            help='Para realizar armazenamento dos dados enviados pela porta serial.')
    args = parser.parse_args()
    try:
        if not args.store and not args.analyze:
            main()
        else:
            main(store=args.store, analyze=args.analyze)
    except KeyboardInterrupt:
        print("\nTecla de escape prescionada.\nAbortando")
