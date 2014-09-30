// Interface de controle da estação fisiológica
// Baseado na estação meterologica
// Centro de Tecnologia Academica - UFRGS
// http://cta.if.ufrgs.br - 

int sensorTemperature = 5;    
float sensorValue = 0; 
bool flag_test= 0;
int frequency = 5;
unsigned long time_0;
float period;
void setup() {
  Serial.begin(115200);
  period = 1.0/frequency;
}
void loop() {
  time_0=millis();
  temperaturaNTC();
  if((period*1000) -(millis()-time_0)<0){
    Serial.println("Frequência muito alta para operação");   
    break;
  }
  delay((period*1000) -(millis()-time_0));
}
void temperatura_NTC()
{
  sensorValue = analogRead(sensorPin);   
  Serial.println(sensorValue);
}
void pulso(){
}
