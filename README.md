# **RESPIRÔMETRO**
[Centro de Tecnologia Acadêmica - UFRGS](http://cta.if.ufrgs.br)

![Alt text](resources/LogoCTA_350px.png)

**Autor/es:** Béuren Felipe Bechlin

**Licença/s:** GPL v3

---
## Descriçao do projeto

O Respirômetro é um equipamento desenhado para medir a frequência respiratória humana. 
Utilizando um par de termistores, o sinal analógico da respiração é convertido em sinal 
digital que pode então ser processado por um microcontrolador que envia dados para o computador.

---
## Primeiros passos

Para utilização do projeto é necessário uma placa de prototipagem Arduino ou um microcontrolador
ATMEGA com suporte a wiring. Na pasta sources você irá encontrar a pasta Arduino que contém o código
fonte deve estar no microcontrolador, já na pasta python contém os códigos fontes para coleta de dados
que são enviados ao computador via comunicação serial gerando um arquivo de log. Nessa mesma pasta
se encontra o arquivo para análise dos dados que foram salvas com a etapa anterior. Lembrando que os
códigos foram desenvolvidos usando *Python* e para seu funcionando é necessário ter instalado o 
interpretador *Python*.
 
### Usando o projeto

#### Passo 1
Primeiro passo a se realizar é instalar as dependências do projeto em sua máquina, caso utiliza
um sistema operacional baseado em GNU/Linux esse trabalho foi reduzido. Supondo que você está
em um ambiente Linux use o seguinte comando:

Esse passo você irá realizar somente uma vez, como é necessário instalar pacotes e módulos python
em seu computador será necessário a senha de administrador para essas operações.

``` Unix
make setup 
```

Após realizar este comando reinicie seu terminal e então realize o segundo passo.

#### Passo 2
Nessa parte será enviado o software para a placa microcontroladora para isso estamos usando
o framework Platformio, lembrando que o firmware desenvolvido foi feito para microcontroladores
ATMEL como suporte a wiring, como por exemplo Arduinos em geral.

``` Unix
make firmware
```

Ao entrar com esse comando irá se iniciar uma tela para seleção da placa que se está usando, além
da porta usb em que ela está conectada ao computador. Na primeira vez que for enviar o firmaware para
cada tipo de placa será necessário digiar _y_ no terminal para que o platformio instale as dependências
para compilação de cada modelo de placa.

---
Para demais informações e documentação completa visite
[CTA - RESPIRÔMETRO](http://cta.if.ufrgs.br/projects/fisiolog/wiki/Respirômetro)
