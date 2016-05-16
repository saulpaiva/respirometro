#ifndef BINARYCOMMUNICATION
#define BINARYCOMMUNICATION

#if (ARDUINO >= 100)
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

/*
    Cria uma comunicação Serial enviando bytes 'crus' para obter melhor
        desempenho. 
    Logo é necessário que onde os dados são recebidos que sejam decodificados,
        já que não estão com caracteres ASCII

    Protocolo para utilização:

        É enviado um byte inicial, indicando quantos bytes vão ser enviados.
        Esse byte é um unsigned int_8b logo é possível endereçar somente 255 bytes.

        X.A.B.C.D
         |-------| : Lenght = X
    
    Melhor forma de usar é criar uma estrutura de dados
    Ex.:
    struct data{
        int x1;
        int x2;
        ...
        char str[10];
        ..
        float xn;
    };  
    
    // Criando objeto para comunicação
    comm = BinCommunication((void*)&data, sizeof(data));
    // Nesse momento você alterar a sua estrutura e cada vez que usar o metodo
    // send() será enviado todos os dados para o computador
    comm.send();
*/
class BinCommunication{
    private:
        /* Tamanho em bytes da banda de dados*/
        int dataLen;
        /* Ponteiro do array de dados*/
        uint8_t *dataPtr;

    public:
        /* Inicializando as variáveis necessárias*/
        BinCommunication(void *dataPtr, int dataLen);
        /* Incializando comunicação Serial do Arduino*/
        void begin(long int baudRate);
        /* Envia os dados que estão no array de dados*/
        bool send();
        /* */
        int getDataLen();
        void setDataLen(int dataLen);
        void* getDataPointer();
        void setDataPointer(void* dataPtr);
};

#endif
