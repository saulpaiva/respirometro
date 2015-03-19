#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Estação biométrica CTA
# Béuren Bechlin
#
# Programa para plot de dados
#
# Centro de Tecnologia Acadêmica - UFRGS
# http://cta.if.ufrgs.br
#
# Licença: GPL v3
# Ordem de argumentos : [arquivo_entrada]
# Onde
# [arquivo_entrada]: arquivo que será visualizado

# Exemplo: python visualiza_estatica.py coleta.log

import numpy as np
import matplotlib.pyplot as plt
import time, sys
parametro = sys.argv[1:]

fisiologfile = open(parametro[0],'r')

# Inicialização de variáveis
contador = 0
x0 = 0
i = 0
x = []
y1 = []
y2 = []
med_y1 = 0
med_y2 = 0
var_y1 = 0
var_y2 = 0

# Importando dados do arquivo e encontrando média
for linha in fisiologfile:
	if linha[0:5] == '#Freq':
		frequencia = float(linha.replace('\n', '').split('\t')[1])
		periodo = 1.0/ frequencia
	elif linha[0] != '#' and linha[0:3] != '0.0':
		y1.append(float(linha.split('\t')[0]))
		y2.append(float(linha.split('\t')[1]))
		x.append(i)
		# Média
		med_y1 += y1[i]
		med_y2 += y2[i]
		i += 1

fisiologfile.close()

# Média e varianca:
med_y1 = med_y1 / len(y1)
med_y2 = med_y2 / len(y2)
for j in xrange(0, len(y1)):
	y1[j] = y1[j] - int(med_y1)
	y2[j] = y2[j] - int(med_y2)
	# Desvio
	var_y1 = (y1[j] - med_y1)*(y1[j] - med_y1)
	var_y2 = (y2[j] - med_y2)*(y2[j] - med_y2)

des_y1 = var_y1**(0.5)
des_y2 = var_y2**(0.5)


maior_abs_y1 = max(y1) if max(y1) + min(y1) > 0 else -min(y1)
maior_abs_y2 = max(y2) if max(y2) + min(y2) > 0 else -min(y2)
# Desvio padrão
for k in xrange(0, len(y1)):
	y1[k] = y1[k]/maior_abs_y1
	y2[k] = y2[k]/maior_abs_y2


plt.figure()
plt.xlim(0,i-1)
plt.ylim(min(y1) if min(y2) > min(y1) else min(y2) , max(y1) if max(y1) > max(y2) else max(y2))
plt.ylabel(u"Tensão")
plt.xlabel(u"Amostras(n)")
plt.grid(True)
plt.subplots_adjust(left=0.13, right=0.9, top=0.9, bottom=0.2)
plt.title('Frequencia Respiratoria')
plt.plot(x,y1)
plt.plot(x,y2)

plt.show()
