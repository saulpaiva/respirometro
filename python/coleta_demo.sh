#!/bin/bash
# Script Biometrica

if [ $# -eq 0 ] ; then
    echo 'ERRO: Faltam argumentos.\nPor favor inicie novamente e passe os argumentos na ordem\n[PORTA_USB] [NOME_SAÍDA] [TEMPO]'
    exit 1
fi
usb_port=$1
log_file=$2
log_file="$log_file.log"
time=$3 
echo "Bem Vindo!\n Esse script realiza o processo padrão para estimar a frequência respiratória."
echo "Dados usados:\n PORTA USB = $usb_port\tNOME DO ARQUIVO = $log_file\tTEMPO DO EXERCÍCIO = $time s"
echo "Iniciando em: \n3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1

echo "python armazenamento_new.py $usb_port 115200 $logfile $time"

python armazenamento_new.py $usb_port 115200 $logfile $time

if [ -f "$log_file" ]
then
	echo "DADOS FORAM ARMAZENADOS COM SUCESSO! \n Iniciando algoritmo para o relatório."
	python visualiza_new.py $log_file 0 $time 2 4 0 1
else
	echo "ERRO! Não foi possivel realizar as operações"
fi

