/*
**********************************************************
*                RESPIRÔMETRO - CTA                      *
**********************************************************
 AUTOR/ES: Béuren F. Bechlin

 Algoritmo desenvolvido para testes rápido para o shield 
 respirômetro v0.20. Nele é testado:
 * LEDS
 * Cartão SD
 * Botões configurados com pullUp interno

       +-------------------------------------------+
       |   Centro de Tecnologia Acadêmica - UFRGS  |
       |         http://cta.if.ufrgs.br            |
       +-------------------------------------------+

 Este arquivo fonte faz parte do Respirômetro e está
 sobre as seguinte/s licença/s:
  * GPL v3
*/

#include <SD.h>
#include "utils.h"

#define CSPin 10
#define btt01Pin 2
#define btt02Pin 3

int ledPin[3] = {4, 7, 8};
int lastRead[2] = {0, 0};
int frequency = 10; //Hz
int period = int(1000.0/frequency); //ms
Interface _interface(loopInterface, period);
Polling _pollingBtt01(20);
Polling _pollingBtt02(20);
File _file; 

void loopInterface(){

    unsigned long time_0 = millis();
    int termRead[2] = {analogRead(A0), analogRead(A1)};
    String read_str = String(String(termRead[0])+"\t"+String(termRead[1]));

    if(termRead[0] - lastRead[0] > 1){
        read_str = String(read_str + "\tInspirando");
        digitalWrite(ledPin[1], HIGH);
        digitalWrite(ledPin[2], LOW);
    }
    else if(termRead[0] - lastRead[0] < -1){
        read_str = String(read_str + "\tExpirando");
        digitalWrite(ledPin[1], LOW);
        digitalWrite(ledPin[2], HIGH);
    }

    _file = SD.open("Resp.txt", FILE_WRITE);
    if(_file){
        _file.println(read_str);    
    }
    else{
        Serial.println("ERRO ao escrever no arquivo.");    
    }
    _file.flush();

    lastRead[0] = termRead[0];
    lastRead[1] = termRead[1];
}

void setup(){

    Serial.begin(9600);

    pinMode(CSPin, OUTPUT);

    if (!SD.begin(CSPin)) 
        return;
    _file = SD.open("Resp.txt", FILE_WRITE);
    
    pinMode(btt01Pin, INPUT_PULLUP);
    attachInterrupt(0, btt01Rising, FALLING);
    
    pinMode(btt02Pin, INPUT_PULLUP);
    attachInterrupt(1, btt02Rising, FALLING);
    
    for(int i = 0; i < 3; i++)
        pinMode(ledPin[i], OUTPUT);

}

void loop(){
    _interface.run();
}

void btt01Rising(){
    if(_pollingBtt01.test()){
        if(!_interface.running()){
            _interface.setState();
            digitalWrite(ledPin[0], HIGH);
            digitalWrite(ledPin[1], LOW);
            digitalWrite(ledPin[2], LOW);
        }
        _pollingBtt01.executed();
    }
}

void btt02Rising(){
    if(_pollingBtt02.test()){
        if(_interface.running()){ 
            _interface.setState();
            for(int i = 0; i < 3; i++)
              digitalWrite(ledPin[i], LOW);
        } 
        _pollingBtt02.executed();       
    }
}

