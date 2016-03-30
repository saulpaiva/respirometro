#include "utils.h"

Polling::Polling(){
    this->period = 0;
}

Polling::Polling(int period){
    this->period = period;
}

bool Polling::test(){
    if(millis() - this->time_last  >= this->period)
        return true;
    else
        return false; 
}

void Polling::executed(){
    this->time_last = millis();
} 

void Polling::setPeriod(int period){
    this->period = period;
}


Interface::Interface(void (*callback)(void), int period){
    this->callback = callback;
    this->state = false;
    this->_interval.setPeriod(period);
    this->_interval.executed();
}

bool Interface::running(){
    return this->state;
}

void Interface::setState(){
    this->state = !this->state;
}

void Interface::run(){
    if(this->state == true){
        if(this->_interval.test()){
            this->callback();
            this->_interval.executed();
        }
    }
}

void Interface::setPeriod(int period){
    this->_interval.setPeriod(period);
}

