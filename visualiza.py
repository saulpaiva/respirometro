 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Visualizador de Temperatura
#

from pylab import *
import time, sys
parametro = sys.argv[1:]

ion()
fisiologfile = open(parametro[0]+'.log','r')

i = 0
t = []
h = []

for linha in fisiologfile:
	if linha[0] == '!':
		frequencia = linha.strip('!')
		periodo = 1.0/ frequencia
	elif linha[0] != '#':
		h.append(float(linha.split('\t')[1]))
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
quantidade_dados = int(intervalo*frequencia(3/2))
variacao = 0.02 #porcento  
variacao_max = 0.20 #porcento

#Inicialização de variáveis
x0 = 0

while True:
	try:
		t0 = time.time()
		
		#Leitura do ultimo dado do arquivo (Problema se o arquivo não estiver sendo atualizado)
		fisiologfile = open(parametro[0]+'.log','r')
		s = fisiologfile.readlines()[-1].split('\t')[1]		
		t.append(i)
		h.append(s)
		line[0].set_data(t,h)
		x0 = i - intervalo
		sub.set_xlim(x0,i)
		
		#Controle do foco da imagem do gráfico
		yf=(1.0 + variacao_y)*(max(h[-quantidade_dados:]))
		yi=(1.0 - variacao_y)*(min(h[-quantidade_dados:]))
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
		fisiologfile.close()
		time.sleep(periodo - (time.time()- t0))
  except KeyboardInterrupt:
    break
  except ValueError:
	print "Não é possível operar a essa frequência (controlador)"
	break
	
