/*
**********************************************************
*                  RESPIRÔMETRO - CTA                    *
**********************************************************
    AUTOR: Béuren F. Bechlin

       +-------------------------------------------+
       |   Centro de Tecnologia Acadêmica - UFRGS  |
       |         http://cta.if.ufrgs.br            |
       +-------------------------------------------+

    Este arquivo fonte faz parte do Respirômetro e está
sobre a licença GPL v3, como também os arquivos:
    * binaryCommunication(.h/.cpp): usado para criar uma
        comunicação com dados binários entre o arduino e 
        o computador e não com CHARS como é o default.
    * utils(.h/.cpp): usado para criar rotinas que devem
        ser executadas com uma frequência fixa, funciona-
        mento análogo com o delay() disponibilizado pela
        plataforma, entretanto não para o processamento
        e sim utiliza metodo de polling para verificar 
        se deve executar algo.

    ENTRADAS ANALÓGICAS:
        A0 :: RESPIRÔMETRO PRIMEIRA ENTRADA
        A1 :: RESPIRÔMETRO SEGUNDA ENTRADA
        A2 :: ELETROCARDIOGRAMA
*/

#include "binaryCommunication.h"
#include "utils.h"

/* Definindo a frequencia de operação do equipamento*/
#define FREQUENCY 250  // Hz
 
/* Criando estruturas de dados para definir como será enviado os 
    dados de comunicação*/
struct{
    short int controlFlag = 0xAAAA; 
    short int frequency = FREQUENCY;;
}headerStruct;

struct{
    short int reads[1];
}dataStruct;

/* Criando comunicação*/
BinCommunication commHeader(&headerStruct, sizeof(headerStruct));
BinCommunication commData(&dataStruct, sizeof(dataStruct));
/* Criando interface que se repetirá a cada '1.0/FREQUENCY'. Essa 
    interface irá chamar a função 'measures' a cada repetição*/
Interface interface(&measures, 1000.0/FREQUENCY);

void setup(){
    /* Iniciando comunicação serial*/
    Serial.begin(115200);
    while(!Serial){
    }

    delay(50);
    commHeader.send();
    delay(50);    
}

void loop(){
    interface.run();
}

void measures(){ 
    for(int i = 0; i < 1; i++)
        dataStruct.reads[i] = analogRead(i);    
    /* Enviando dados*/
    commData.send();      
}
