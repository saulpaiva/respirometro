#include "binaryCommunication.h"

BinCommunication::BinCommunication(void *dataPtr, int dataLen){ 
    this->dataPtr = (char*)dataPtr;
    this->dataLen = dataLen;    
}

void BinCommunication::begin(long int baudRate){
    Serial.begin(baudRate);
}

bool BinCommunication::send(){
    Serial.write(this->dataLen);
    if(Serial.write(this->dataPtr, this->dataLen) == this->dataLen)
        return true;
    return false;
}

int BinCommunication::getDataLen(){
    return this->dataLen;
}

void BinCommunication::setDataLen(int dataLen){
    this->dataLen = dataLen;
}

void* BinCommunication::getDataPtr(){
    return this->dataLen;
}

void BinCommunication::setDataPtr(void* dataPtr){
    this->dataPtr = (char*) dataPtr;
}
