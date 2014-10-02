#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Estação biométrica CTA
#
# Programa para visualização dos dados
# Este programa é utilizado com o programa biometrica.ino no qual a taxa de amostragem é definida no microcontrolador
# 
# Centro de Tecnologia Acadêmica - UFRGS
# http://cta.if.ufrgs.br
#
# Licença: GPL v3
# Ordem de argumentos : [arquivo_entrada]
# Onde 
# [arquivo_entrada]: arquivo que será visualizado

# Exemplo: python visualiza.py coleta1.log

from pylab import *
import time, sys
parametro = sys.argv[1:]

ion()
fisiologfile = open(parametro[0],'r')

i = 0
t = []
h = []

for linha in fisiologfile:
	if linha[0:5] == '#Freq':
		frequencia = float(linha.replace('\n', '').split('\t')[1])
		periodo = 1.0/ frequencia
	elif linha[0] != '#':
		h.append(float(linha))
		t.append(i)
		i = i + periodo
	
fisiologfile.close()

fig = figure(1)
sub = subplot(111)

line = plot(t, h, 'r-')

xlabel('Tempo(s)')
ylabel('')
title('Frequência Respiratória')

#Variáveis de controle
intervalo = 5
quantidade_dados = int(intervalo*frequencia*(3/2))
variacao = 0.02 #porcento  
variacao_max = 0.20 #porcento

#Inicialização de variáveis
x0 = 0

while True:
	try:
		t0 = time.time()
		
		#Leitura do ultimo dado do arquivo (Problema se o arquivo não estiver sendo atualizado)
		fisiologfile = open(parametro[0],'r')
		s = float(fisiologfile.readlines()[-1])	
		fisiologfile.close()		
		t.append(i)
		h.append(s)
		line[0].set_data(t,h)
		x0 = i - intervalo
		sub.set_xlim(x0,i)
		
		#Controle do foco da imagem do gráfico
		yf=(1.0 + variacao)*(max(h[-quantidade_dados:]))
		yi=(1.0 - variacao)*(min(h[-quantidade_dados:]))
		valor_medio= sum(h[-quantidade_dados:])/quantidade_dados
		if(yf > (1 + variacao + variacao_max)*valor_medio):
			yf = (1 + variacao + variacao_max)*valor_medio
		if(yi < (1 - variacao - variacao_max)*valor_medio):
			yi = (1 - variacao - variacao_max)*valor_medio
		sub.set_ylim(yi,yf)
		
		draw()	
		i = i+periodo

		if (periodo - (time.time()- t0))< 0:
			print "Não é possível operar a essa frequência"
			break 				
		time.sleep(periodo - (time.time()- t0))
	except KeyboardInterrupt:
    		break
	except ValueError:
		print "Não é possível operar a essa frequência (controlador)"
		break
	
