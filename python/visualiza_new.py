#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 Estação biométrica CTA
 Béuren Bechlin

 Programa para estimar a frequência respiratória

 Centro de Tecnologia Acadêmica - UFRGS
 http://cta.if.ufrgs.br

 Licença: GPL v3
 Ordem de argumentos : [arquivo_entrada], [instante inicial], [instante final],
    [tipo do filtro], [repetições], [freq_inicial], [freq_final]
 Onde:

  -Evidenciando arquivo onde estão os dados a serem anilizado/exibidos:
	[arquivo_entrada]: arquivo que será visualizado/analisado.

  -Determinando em que ponto da amostra quer ser analizado:
    [instante inicial](s): instante para iniciar a visualização/analise.
	[instante final](s): instante para finalizar a visualização/analise.

  -Escolhendo filtro apropriado:
    [tipo do filtro]: escolher o filtro a ser utilizado no processo. (1 ou 2)
	[repetições]: definir a quantidade de vezes que o filtro será utilizado.

  -Definindo o espectro de frequência a se uso:
    [freq_inicial](Hz): definir a frequência inicial positiva que será usada, isso
        influenciará na precisão do resultado para o método.
    [freq_final](Hz): definir a frequência final positiva que será usada, lembrando
        que pela definição de transformada de fourier o domínio do espectro de
        frequência não será maior que a frequência de obtenção desses dados
        divido por 2, ou seja, a as frequências definidas aqui devem estar no
        intervalo [0;freq/2]
'''
# Exemplo: python visualiza_new.py coleta_Nome_Exemplo_1min.log 0 60 2 4 0 7
from array import *
from scipy.fftpack import fft, fftfreq, fftshift
import numpy as np
import Image
import sys
import matplotlib.pyplot as plt
import math

# Atribuindo as váriaveis com os valores de entrada
parametro = sys.argv[1:]
log_file = parametro[0]
fisiologfile = open(log_file,'r')
t_inicial = int(parametro[1])
t_final = int(parametro[2])
n_filtro = int(parametro[3])
qtd_filtro = int(parametro[4])
freq_i = float(parametro[5])
freq_f = float(parametro[6])
png_name = 'Resp_'+log_file.split('_')[1]+'_'+str(t_inicial)+'_a_'+str(t_final)+'_'+str(int(freq_i))+'_a_'+str(int(freq_f))+'.png'
user_name = parametro[0].replace('_', ' ').split(' ')[1] + ' ' + parametro[0].replace('_', ' ').split(' ')[2]
# TROCAR!!!
freq = int(fisiologfile.readline().split('\t')[1])


# Inicialização de variáveis
x1 = array('f', [])
y1 = array('f', [])
y2 = array('f', [])
y1_filt = array('f', [])
y2_filt = array('f', [])
x_fft_plot = array('f', [])
y1_fft_plot = array('f', [])
y2_fft_plot = array('f', [])
x_fft = array('f', [])
y1_fft = array('f', [])
y2_fft = array('f', [])


med_y1 = 0
med_y2 = 0
var_y1 = 0
var_y2 = 0

N_i = 0
N_f = 0
sum_int_1 = 0
sum_int_2 = 0
sum_norm_1 = 0
sum_norm_2 = 0

cont_ini = t_inicial*freq
cont_final = t_final*freq

N = cont_final - cont_ini
T = 1.0/freq
dx = float(freq)/N

i = 0
date_time = 0

# Importando dados do arquivo e encontrando média
for linha in fisiologfile:
    if linha[0] != '#':
    	if (i >= cont_ini and i < cont_final):
            y1.append(int(linha.split('\t')[0]))
            y2.append(int(linha.split('\t')[1]))
            x1.append(i*T)
    	i += 1
    elif linha[0:7] == '#Coleta':
        date_time_d = linha.split(' ')[5]
        date_time_d = date_time_d.split('-')[2]+ '/' + date_time_d.split('-')[1]+ '/' + date_time_d.split('-')[0]
        date_time_h = linha.replace('\n','').split(' ')[6]

fisiologfile.close()

# Média e varianca:
med_y1 = sum(y1) / len(y1)
med_y2 = sum(y2) / len(y2)
maior_abs_y1 = med_y1 - (max(y1) if max(y1) + min(y1) > 2*med_y1 else min(y1))
maior_abs_y2 = med_y2 - (max(y2) if max(y2) + min(y2) > 2*med_y2 else min(y2))
for j in xrange(0, len(y1)):
	y1[j] = (y1[j] - med_y1)/maior_abs_y1
	y2[j] = (y2[j] - med_y2)/maior_abs_y2
	# Desvio:
	var_y1 += y1[j] * y1[j]
	var_y2 += y2[j] * y2[j]
	y1_filt.append(y1[j])
	y2_filt.append(y2[j])

var_y1 /= len(y1)
var_y2 /= len(y2)
var_med = (var_y1 + var_y2)/2
des_y1 = var_y1**(0.5)
des_y2 = var_y2**(0.5)
des_med = (var_med)**(0.5)

# Filtro:
if(n_filtro == 1):
	for n in xrange(1,qtd_filtro):
		for k in xrange(1, len(y1) - 2):
			y1_filt[k] = (y1_filt[k-1] + y1_filt[k] + y1_filt[k+1])/3
			y2_filt[k] = (y2_filt[k-1] + y2_filt[k] + y2_filt[k+1])/3
elif(n_filtro == 2):
	for n in xrange(1,qtd_filtro):
        	y1_filt[1] = (y1_filt[0] + y1_filt[1] + y1_filt[2])/3
		y2_filt[1] = (y2_filt[0] + y2_filt[1] + y2_filt[2])/3
		for k in xrange(2, len(y1) - 3):
			y1_filt[k] = (y1_filt[k-2] + y1_filt[k-1] + y1_filt[k] + y1_filt[k+1] + y1_filt[k+2])/5
			y2_filt[k] = (y2_filt[k-2] + y2_filt[k-1] + y2_filt[k] + y2_filt[k+1] + y2_filt[k+2])/5
            	y1_filt[len(y1) - 2] = (y1_filt[len(y1) - 3] + y1_filt[len(y1) - 2] + y1_filt[len(y1)-1])/3
        	y2_filt[len(y2) - 2] = (y2_filt[len(y2) - 3] + y2_filt[len(y2) - 2] + y2_filt[len(y2)-1])/3

# Transformada de fourier:
#   yn_fft x_fft: realizam a trasnformada de fourier no espectro de frequência
#   yn_fft_plot x_fft_plot: inicialmente é usado um 'shift'(deslocamento) para jogar as
#       componentes negativas que estão após as componentes positivas quando usamos
#       numpy.fft.fftshift, para o início do array.
#   yn_fft_plot x_fft_plot: são usados novamente para agora selecionar somente as frequências
#       positivas e suas componentes

y1_fft = fft(y1_filt)
y2_fft = fft(y2_filt)
x_fft = fftfreq(N, T)
x_fft_plot = fftshift(x_fft)
x_fft_plot = x_fft_plot[N/2:N]
y1_fft_plot = fftshift(y1_fft)
y2_fft_plot = fftshift(y2_fft)
y1_fft_plot = np.abs(y1_fft_plot[N/2:N])
y2_fft_plot = np.abs(y2_fft_plot[N/2:N])


# Transformada de fourier na metade de todo período:
N_half = int(N/2)
t_half = (t_final - t_inicial)/2

x_half_fft = fftfreq(N_half, T)
x_half_fft = fftshift(x_half_fft)
x_half_fft = x_half_fft[math.floor(N_half/2):N_half]


y1_half_1_fft = fft(y1_filt[0:N_half])
y2_half_1_fft = fft(y2_filt[0:N_half])

y1_half_1_fft = fftshift(y1_half_1_fft)
y2_half_1_fft = fftshift(y2_half_1_fft)

y1_half_1_fft = np.abs(y1_half_1_fft[math.floor(N_half/2):N_half])
y2_half_1_fft = np.abs(y2_half_1_fft[math.floor(N_half/2):N_half])


y1_half_2_fft = fft(y1_filt[N_half:N])
y2_half_2_fft = fft(y2_filt[N_half:N])

y1_half_2_fft = fftshift(y1_half_2_fft)
y2_half_2_fft = fftshift(y2_half_2_fft)

y1_half_2_fft = np.abs(y1_half_2_fft[math.floor(N_half/2):N_half])
y2_half_2_fft = np.abs(y2_half_2_fft[math.floor(N_half/2):N_half])

# MATH.FLOOR para conter o 0
# Determinando momento das distribuições:
#   N através da frequência já que também depende da frequência, N = tempo da amostra*freq
#       dessa forma as razões entre eles são constantes
#   N/F = F.tempo/F = tempo -> N'/F' = N/F

N_i = freq_i*N/freq
N_f = freq_f*N/freq

for i in xrange(int(N_i),int(N_f)):
	aux_1 = y1_fft_plot[i]*y1_fft_plot[i]*y1_fft_plot[i]*dx
	aux_2 = y2_fft_plot[i]*y2_fft_plot[i]*y2_fft_plot[i]*dx

	sum_int_1 += aux_1*x_fft_plot[i]
	sum_int_2 += aux_2*x_fft_plot[i]

	sum_norm_1 += aux_1
	sum_norm_2 += aux_2

first_moment_1 = sum_int_1 / sum_norm_1
first_moment_2 = sum_int_2 / sum_norm_2
first_moment_med = (first_moment_1 + first_moment_2)/2
t_est_1 = 1.0/first_moment_1
t_est_2 = 1.0/first_moment_2
t_est_med = 1.0/first_moment_med

N_i = freq_i*N_half/freq
N_f = freq_f*N_half/freq

sum_int_1 = 0
sum_int_2 = 0
sum_norm_1 = 0
sum_norm_2 = 0

for i in xrange(int(N_i),int(N_f)):
	aux_1 = y1_half_1_fft[i]*y1_half_1_fft[i]*y1_half_1_fft[i]*dx
	aux_2 = y2_half_1_fft[i]*y2_half_1_fft[i]*y2_half_1_fft[i]*dx

	sum_int_1 += aux_1*x_half_fft[i]
	sum_int_2 += aux_2*x_half_fft[i]

	sum_norm_1 += aux_1
	sum_norm_2 += aux_2

first_moment_1_half_1 = sum_int_1 / sum_norm_1
first_moment_2_half_1 = sum_int_2 / sum_norm_2
first_moment_med_half_1 = (first_moment_1_half_1 + first_moment_2_half_1)/2
t_est_1_half_1 = 1.0/first_moment_1_half_1
t_est_2_half_1 = 1.0/first_moment_2_half_1
t_est_med_half_1 = 1.0/first_moment_med_half_1

sum_int_1 = 0
sum_int_2 = 0
sum_norm_1 = 0
sum_norm_2 = 0

for i in xrange(int(N_i),int(N_f)):
	aux_1 = y1_half_2_fft[i]*y1_half_2_fft[i]*y1_half_2_fft[i]*dx
	aux_2 = y2_half_2_fft[i]*y2_half_2_fft[i]*y2_half_2_fft[i]*dx

	sum_int_1 += aux_1*x_half_fft[i]
	sum_int_2 += aux_2*x_half_fft[i]

	sum_norm_1 += aux_1
	sum_norm_2 += aux_2

first_moment_1_half_2 = sum_int_1 / sum_norm_1
first_moment_2_half_2 = sum_int_2 / sum_norm_2
first_moment_med_half_2 = (first_moment_1_half_2 + first_moment_2_half_2)/2
t_est_1_half_2 = 1.0/first_moment_1_half_2
t_est_2_half_2 = 1.0/first_moment_2_half_2
t_est_med_half_2 = 1.0/first_moment_med_half_2

# Configuração plot
# h1 = fonts[0], h2 ...
fontsize = [20, 18 ,16, 14, 12]
color = ['Blue', 'Green', 'Yellow', 'Red']

# Criando figura do tamanho A4
plt.figure(1, figsize=(8.27, 11.7))
fig = plt.gcf()
fig.canvas.set_window_title(u'Frequência Respiratória[CTA]\tN1:%f, N2:%f'% (first_moment_1, first_moment_2))
fig.suptitle(u'Frequência Respiratória:\n',
        fontsize=fontsize[2],
        fontweight='bold')

sub_plot1 = plt.subplot(3,1,1)
plt.text(0, 1.1, u'Nome: %s                        Data da coleta: %s' % (user_name, date_time_d),
        horizontalalignment='left',
        fontsize=fontsize[3],
        transform = sub_plot1.transAxes)
plt.text(0, 1.01, u'Horário da Coleta: %s              Tempo analisado %s s à %s s' % (date_time_h, str(t_inicial), str(t_final)),
        horizontalalignment='left',
        fontsize=fontsize[3],
        transform = sub_plot1.transAxes)
plt.ylim(-1,1)
plt.plot(x1,y1_filt,
        label = 'Narina Direita',
        color = color[0])
plt.plot(x1,y2_filt,
        label = 'Narina Esquerda',
        color = color[1])
plt.ylabel(u"Tensão Normalizada y(t)",
        fontsize = fontsize[4])
plt.xlabel(u"Tempo t(s)",
        fontsize = fontsize[4])
plt.grid(True)

sub_plot2 = plt.subplot(3,1,2)

plt.xlim(freq_i, freq_f)
plt.plot(x_fft_plot,  (1.0/N)*y1_fft_plot,
        label = 'Narina Direita',
        color = color[0])
plt.plot(x_fft_plot,  (1.0/N)*y2_fft_plot,
        label = 'Narina Esquerda',
        color = color[1])
plt.ylabel(u"|Y(f)|",
        fontsize = fontsize[4])
plt.xlabel(u"Frequência f(Hz)",
        fontsize = fontsize[4])
sub_plot2.legend(loc='upper right',
        fancybox=True,
        framealpha=0.5)
plt.grid(True)

sub_plot3 = plt.subplot(3,1,3)
sub_plot3.patch.set_visible(False)
sub_plot3.axis('off')

im = Image.open('logo.png')
plt.figimage(im,2250, 175)

# Item Resultados:
plt.text(0,0.9,u'Resultados: \n', fontsize=fontsize[0], fontweight='bold')
plt.text(0,0.84,u'   Relativo ao intervalo de %.2f segundos à %.2f segundos: \n' % (t_inicial, t_final), fontsize=fontsize[4], fontweight='bold')
plt.text(0,0.78,u'          Narina direita:', fontsize=fontsize[4], fontweight='bold')
plt.text(0.4,0.70,u'%.4f            %.3f            %.3f          %.3f\n' % (first_moment_1, t_est_1, var_y1, des_y1), fontsize=fontsize[4])
plt.text(0,0.72,u'          Narina esquerda:', fontsize=fontsize[4], fontweight='bold')
plt.text(0.4,0.64,u'%.4f            %.3f            %.3f          %.3f\n' % (first_moment_2, t_est_2, var_y2, des_y2), fontsize=fontsize[4])
plt.text(0,0.66,u'          Média total:', fontsize=fontsize[4], fontweight='bold')
plt.text(0.4,0.58,u'%.4f            %.3f            %.3f          %.3f\n' % (first_moment_med, t_est_med, var_med, des_med), fontsize=fontsize[4])
plt.text(0.38,0.58,u'Frequência       Período        Variância       Desvio', fontsize=fontsize[4], fontstyle = 'italic')
plt.text(0.42,0.52,u'(Hz)                (s)                                  Padrão', fontsize=fontsize[4], fontstyle = 'italic')

plt.text(0,0.38,u'   Relativo ao intervalo: \n', fontsize=fontsize[4], fontweight='bold')
plt.text(0.40,0.38,u'%.2f s a %.2f s            %.2f s a %.2f s' % (t_inicial, t_half, t_half, t_final), fontsize=fontsize[4], fontweight='bold')
plt.text(0,0.32,u'          Narina direita:', fontsize=fontsize[4], fontweight='bold')
plt.text(0.4,0.24,u'%.4f            %.3f            %1.3f          %.3f\n' % (first_moment_1_half_1, t_est_1_half_1, first_moment_1_half_2, t_est_1_half_2), fontsize=fontsize[4])
plt.text(0,0.26,u'          Narina esquerda:', fontsize=fontsize[4], fontweight='bold')
plt.text(0.4,0.18,u'%.4f            %.3f            %.3f          %.3f\n' % (first_moment_2_half_1, t_est_2_half_1, first_moment_2_half_2, t_est_2_half_2), fontsize=fontsize[4])
plt.text(0,0.20,u'          Média total:', fontsize=fontsize[4], fontweight='bold')
plt.text(0.4,0.12,u'%.4f            %.3f            %.3f          %.3f\n' % (first_moment_med_half_1, t_est_med_half_1, first_moment_med_half_2, t_est_med_half_2), fontsize=fontsize[4])
plt.text(0.38,0.12,u'Frequência       Período        Frequência       Período', fontsize=fontsize[4], fontstyle = 'italic')
plt.text(0.42,0.06,u'(Hz)                (s)                   (Hz)                (s)', fontsize=fontsize[4], fontstyle = 'italic')

plt.subplots_adjust(left = 0.1 ,right = 0.9 ,bottom=0.1, top = 0.9 ,wspace = 0.3, hspace = 0.3)
fig.savefig(png_name, dpi=400)
#plt.show()
