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
        int getPeriod();
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
        int getPeriod();
        
};

#endif
