#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# Visualizador de dados da estação biométrica
# 
# Centro de Tecnologia Acadêmica - UFRGS
# http://cta.if.ufrgs.br
#
# Licença: GPL v3


from matplotlib import pyplot as plt
import numpy as np
import sys

#Ordem de parametros : [arquivo], [real_time(-R)]
parametro = sys.argv[1:]

#try:
#         filename = sys.argv[1]
#    except:
#         print 'Necessário fornecer um parâmetro: nome do arquivo'
#         sys.exit(1)


fisiologfile = open(parametro[0]+'.log', 'r')

x= []
y= []

for line in fisiologfile:
	line = line.strip()
	if line[0] != "#":
		aux = line.split('\t')	
		x.append(aux[0][-5:-3])
		y.append(aux[1])

plt.plot(x,y)

plt.title("Plot exemplo")
plt.xlabel("Tempo")
plt.ylabel("Freq.")

plt.show()
