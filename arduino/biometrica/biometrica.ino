// Interface de controle da estação fisiológica
// Baseado na estação meterologica
// Centro de Tecnologia Academica - UFRGS
// http://cta.if.ufrgs.br - 

/*
    Protocolo:
        0x01 para erro de frequência de operação muito alta para o processador do microcontrolador.

        0x0A para indicar que o microcontrolar irá enviar os dados dos termistores em dupla, seṕarados por \n.


*/

#define TERM_PIN_1  A0
#define TERM_PIN_2  A1
    
int frequency = 5;
unsigned long time_0;
float period;

void setup() 
{
  Serial.begin(115200);
  period = 1.0/frequency;
  Serial.println(frequency);
  delay(10);
}
void loop() 
{
  time_0 = millis();
  tensao_NTC();
  if((period*1000) -(millis()-time_0) < 0){
    Serial.write(0x01);   
  }
  else{
    delay((period*1000) -(millis()-time_0));
  }
}
void tensao_NTC()
{
  int sensor_value1, sensor_value2; 

  sensor_value1 = analogRead(TERM_PIN_1);   
  sensor_value2 = analogRead(TERM_PIN_2);   

  Serial.write(0x0A);
  Serial.println(sensor_value1);
  Serial.println(sensor_value2);
}
void pulso(){
}
