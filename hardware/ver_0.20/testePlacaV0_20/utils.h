#ifndef UTILS
#define UTILS

#if (ARDUINO >= 100)
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

class Polling{
    private:
        unsigned long time_last;
        int period;
    
    public:
        Polling();
        Polling(int);
        bool test();
        void executed();
        void setPeriod(int);
};

class Interface{
    private:
        bool state;
        void (*callback)(void);
        Polling _interval; 

    public:
        Interface(void (*)(), int);
        
        bool running();
        void setState();
        void setPeriod(int period);
        void run();
        
};

//  * Classe para gerenciar o cartão SD e os arquivos nele

// class SDmanager: public SD{
//     private:
//         String file_name;
//         File data_file;

//     public:
// };

#endif
