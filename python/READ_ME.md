# Estação Biométrica

`Centro de Tecnologia Acadêmica - UFRGS`
http://cta.if.ufrgs.br

![Alt text](python/logo.png)

`Licença: GPL v3`

`Autor: Béuren F. Bechlin`

## Documentação de uso

### Arduino

 Inicialmente é necessário fazer upload do sketch biometrica.ino para seu micro-
controlador arduino.

---

### Python

Para o perfeito funcionamento dos algoritmos é necessário ter um interpretador
de python com pelo menos a versão 2.7 instalada em sua máquina. Além disso,
alguns módulos de python são necessários:

* python-scipy
* python-tk (tkInter)
* python-matplotlib
* python-serial

```
sudo apt-get install python-scipy python-tk python-matplotlib python-serial 
```
---

#### Armazenamento.py

Programa para aquisição dos dados do Arduino salvando-os em um arquivo .log.

Este programa é utilizado com o programa biometrica.ino no qual a taxa de
amostragem é definida no microcontrolador.

Ordem de argumentos : [porta],[taxa_transmissão],[arquivo_saída]
Onde:
1. porta: porta serial no qual o arduino está conectado
2. taxa_transmissão: velocidade de comunicação serial
3. arquivo_saída: nome do arquivo em que os dados serão salvos
4. tempo_de_execução: tempo total de execução, em segundos

PADRÃO NOME DO ARQUIVO DE SAÍDA: coleta_[Nome]_[Sobrenome]_[obs].log
[obs] são observações caso sejam necessárias

Lembrando também que a taxa de transmissão(Baud Rate) da comunicação serial tem
de ser multiplo par de 300. Exemplo 1200, 9600.

---

#### Visualiza.py

Programa que estima e emite um relatório sobre a frequência respiratória. Lembrando
que quanto menor o tempo amostrado maior a imprecisão do método. Além disso, o tempo
mínimo de amostragem é 5s.

Ordem de argumentos : [arquivo_entrada], [instante inicial], [instante final],
[tipo do filtro], [repetições], [freq_inicial], [freq_final]

Onde:

1. Evidenciando arquivo onde estão os dados a serem anilizado/exibidos:
	1. arquivo_entrada: arquivo que será visualizado/analisado.

2. Determinando em que ponto da amostra quer ser analizado:
	1. instante inicial(s): instante para iniciar a visualização/analise.
	2. instante final(s): instante para finalizar a visualização/analise.

3. Escolhendo filtro apropriado:
	1. tipo do filtro: escolher o filtro a ser utilizado no processo. (1 ou 2)
	2. repetições: definir a quantidade de vezes que o filtro será utilizado.

4. Definindo o espectro de frequência a se uso:
	1. freq_inicial(Hz): definir a frequência inicial positiva que será usada, isso
influenciará na precisão do resultado para o método.
	2. freq_final(Hz): definir a frequência final positiva que será usada, lembrando
que pela definição de transformada de fourier o domínio do espectro de frequência
não será maior que a frequência de obtenção desses dados divido por 2, ou seja,
a as frequências definidas aqui devem estar no intervalo [0;freq/2].