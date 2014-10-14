#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Estação biométrica CTA
# Béuren Bechlin
#
# Programa para determinar a máxima frequência de operação da visualização
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

t0 = time.time() ##
ion()
fisiologfile = open(parametro[0],'r')
datafile = open('delay_visu.log','w') ##

#Inicialização de variáveis
contador = 0
x0 = 0
i = 0
x = []
y = []

#Dados para plot
fig = figure(1)
sub = subplot(111)
line = plot(x, y, 'r-')
xlabel('Tempo(s)')
ylabel('Temperatura')
title('Frequencia Respiratoria')

for linha in fisiologfile:
	if linha[0:5] == '#Freq':
		frequencia = float(linha.replace('\n', '').split('\t')[1])
		periodo = 1.0/ frequencia
	elif linha[0] != '#' and linha[0:3] != '0.0':
		y.append(float(linha))
		x.append(i)
		i = i + periodo

fisiologfile.close()

# ---- 
# Variáveis de controle
#
# intervalo: é o intervalo de tempo no eixo X que será plotado dado em *segundos*. 
# quantidade_dados: quantidade de dados usados para estimar o foco do gráfico. Usando os dados mostrados na tela e 50% dos anteriores.
# variacao: determina quanto de variação será usada acima do maior valor e abaixo do menor. Exemplo (1+0.02)=102% do maior valor usado na  # 	estimativa.
# variacao_max: ajuda a conter variações bruscas na escala do gráfico, determina o maior e menor valor que o gráfico
#	irá modificar por ciclo. Exemplo: um dado é maior que os anteriores e posteriores e também está no range do dos dados analisados, #	então o algoritmo irá usar essa definição de porcentagem para relacionar com a média dos valores e definir o novo range Y. 
# frequencia_foco: determina a frequência em que é executado a rotina do foco.
#
# ----

intervalo = 10
quantidade_dados = int(intervalo*frequencia*(1.5))
variacao = 0.02
variacao_max = 0.30
frequencia_foco = 5
frequencia_limpa = 10

yf = (1.0 + variacao)*(max(y))
yi = (1.0 - variacao)*(min(y))
contador = 0
datafile.write('#Tempo de execução inicial (fora do laço): '+str((time.time()- t0)*1000)) ##
print (time.time()- t0)*1000 ##
while True:
	try:
		t0 = time.time()
		contador = contador + 1;
		
		#Leitura do ultimo dado do arquivo, caso o arquivo não esteja sendo atualizado será sempre pego a última linha.
		fisiologfile = open(parametro[0],'r')
		s = float(fisiologfile.readlines()[-1])	
		fisiologfile.close()		
		x.append(i)
		y.append(s)
		line[0].set_data(x,y)
		x0 = i - intervalo
				
		#Controle do foco da imagem do gráfico:
		if (contador % frequencia_foco == 0) :
			if(quantidade_dados > len(y)) :
				yf = (1.0 + variacao)*(max(y[-len(y):]))
				yi = (1.0 - variacao)*(min(y[-len(y):]))
				valor_medio = sum(y[-len(y):])/(len(y))
			else :	
				yf = (1.0 + variacao)*(max(y[-quantidade_dados:]))
				yi = (1.0 - variacao)*(min(y[-quantidade_dados:]))
				valor_medio = sum(y[-quantidade_dados:])/(quantidade_dados)
			if(yf > (1 + variacao + variacao_max)*valor_medio):
				yf = (1 + (variacao + variacao_max))*valor_medio
			if(yi < (1 - (variacao + variacao_max))*valor_medio):
				yi = (1 - (variacao + variacao_max))*valor_medio

		#Limpar a lista, já que dependendo do tempo de execução seu tamanho pode ser muito grande. 
		if (contador % frequencia_limpa  == 0):
			del x [0:-quantidade_dados]
			del y [0:-quantidade_dados]
					
		sub.set_xlim(x0,i)
		sub.set_ylim(yi,yf)
		draw()	
		i = i + periodo

		if (periodo - (time.time()- t0))< 0:
			print "Não é possível operar a essa frequência"
			break 	
			
		datafile.write(str(contador)+"\t"+str((time.time()- t0)*1000)+"\n") ##
		time.sleep(periodo - (time.time()- t0))
	except KeyboardInterrupt:
    		break
	except ValueError:
		print "Não é possível operar a essa frequência (controlador)"
		break
