#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Estação biométrica CTA
#
# Programa para estimar a frequência respiratória
# Este programa é utilizado em conjunto com armazenamento de dados, onde nessa etapa é utilizado os dados para realizar a Trans. de Fourier para estimar frequência respiratória.
# 
# Centro de Tecnologia Acadêmica - UFRGS
# http://cta.if.ufrgs.br
#
# Licença: GPL v3
# Ordem de argumentos : [arquivo_de_dados]
# Onde: 
# [arquivo_de_dados]: nome do arquivo que foram salvos os dados

# Exemplo: python armazenamento.py '/dev/ttyACM0' 115200 coleta1.log 

from scipy.fftpack import fft, fftfreq, fftshift
import matplotlib.pyplot as plt
import numpy as np
import sys

print "---- Programa para estimar a frequência respiratória ---- "
print " Selecionar a quantidade de dados: "

t_inicial = input('Instante inicial (em segundos): ')
t_final = input('Instante final (em segundos): ')


fisiologfile = open(sys.argv[1],'r')
freq = float(fisiologfile.readline().replace('\n', '').split('\t')[1])

cont_ini = t_inicial*freq
cont_final = t_final*freq
y[]
i = -3 # USANDO 3 LINHAS DE COMENTÁRIO NO ARQUIVO
for line in fisiologfile:
	i ++ 
	if(i > cont_ini and i <= cont_final):
		y.append(int(line))

	
# Número de sinais coletados
N = cont_final - cont_ini
# Espaçamento padrão
T = 1.0 / freq
# Eixo X
x = np.linspace(0.0, N*T, N)

# Transformadas
yf = fft(y)
xf = fftfreq(N, T)
xplot = fftshift(xf)
yplot = fftshift(yf)
xplot  = xplot[N/2:N]
yplot  = np.abs(yplot[N/2:N])

# Filtro cúbico de dados (Pensar se deve ser normalizado apartir do maior valor)
y_filtrado = yplot*yplot*yplot  
flag = 1
for i in xrange(0, N/2):
	if xplot[i] > 0.3 and flag == 1:
		 ini = i
		 flag = 0
	if xplot[i] > 1:
		 fim = i
		 break
		 
# Integral
soma_int = 0
soma_norma = 0
dx = freq / N
for i in xrange(ini, fim):
	aux = y_filtrado[i]*dx
	soma_int += aux*xplot[i]
	soma_norma + = aux
first_moment = soma_int / soma_norma 
print first_moment

# Plot
plt.subplot(211)
plt.plot(x, y)
plt.subplot(212)
plt.plot(xplot, (1.0/N) * yplot)
plt.grid()
plt.show()

