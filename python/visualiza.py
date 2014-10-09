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

#Inicialização de variáveis
contador = 0
x0 = 0
i = 0
t = []
h = []

#Dados para plot
fig = figure(1)
sub = subplot(111)
line = plot(t, h, 'r-')
xlabel('Tempo(s)')
ylabel('Temperatura')
title('Frequencia Respiratoria')


for linha in fisiologfile:
	if linha[0:5] == '#Freq':
		frequencia = float(linha.replace('\n', '').split('\t')[1])
		periodo = 1.0/ frequencia
	elif linha[0] != '#' and linha[0] != '0.0':
		h.append(float(linha))
		t.append(i)
		i = i + periodo
	
fisiologfile.close()

#Variáveis de controle

#intervalo: é o intervalo de tempo no eixo X que será plotado
intervalo = 10 #segundos
#quantidade_dados: quantidade de dados usados para estimar o foco do gráfico. Usando 66% dos dados mostrado na tela
quantidade_dados = int(intervalo*frequencia*(3/2))
#variacao: determina quanto de variação será usada acima do maior valor e abaixo do menor. Exemplo (1+0.02)=102% do maior valor usado na estimativa
variacao = 0.02   
variacao_max = 0.20 
frequencia_foco = int(frequencia*intervalo*(0.25))
frequencia_limpagem =  int(frequencia*intervalo*(50) )

yf=(1.0 + variacao)*(max(h))
yi=(1.0 - variacao)*(min(h))
while True:
	try:
		t0 = time.time()
		contador = contador + 1;
		
		#Leitura do ultimo dado do arquivo (Problema se o arquivo não estiver sendo atualizado)
		fisiologfile = open(parametro[0],'r')
		s = float(fisiologfile.readlines()[-1])	
		fisiologfile.close()		
		t.append(i)
		h.append(s)
		line[0].set_data(t,h)
		x0 = i - intervalo
				
		#Controle do foco da imagem do gráfico 
		if (contador % frequencia_foco == 0) :
			yf=(1.0 + variacao)*(max(h[-quantidade_dados:]))
			yi=(1.0 - variacao)*(min(h[-quantidade_dados:]))
			valor_medio= sum(h[-quantidade_dados:])/quantidade_dados
			if(yf > (1 + variacao + variacao_max)*valor_medio):
				yf = (1 + variacao + variacao_max)*valor_medio
			if(yi < (1 - variacao - variacao_max)*valor_medio):
				yi = (1 - variacao - variacao_max)*valor_medio
		#Limpar a lista, já que dependendo do tempo de execução seu tamanho pode ser muito grande
		if (contado % frequencia_limpagem  == 0):
			
					
		sub.set_xlim(x0,i)
		sub.set_ylim(yi,yf)
		draw()	
		i = i+periodo

		if (periodo - (time.time()- t0))< 0:
			print "Não é possível operar a essa frequência"
			break 				
		time.sleep(periodo - (time.time()- t0))
	except KeyboardInterrupt:
    		break
	#except ValueError:
	#	print "Não é possível operar a essa frequência (controlador)"
	#	break
