// Interface de controle da estação fisiológica
// Baseado na estação meterologica
// Centro de Tecnologia Academica - UFRGS
// http://cta.if.ufrgs.br - 

int sensorTemperature = 5;    
float sensorValue = 0; 
int frequency = 5;
unsigned long time_0;
float period;

void setup() 
{
  Serial.begin(115200);
  period = 1.0/frequency;
  Serial.println(frequency);
  delay(50);
}
void loop() 
{
  time_0=millis();
  temperatura_NTC();
  if((period*1000) -(millis()-time_0) < 0)
  {
    Serial.println("Erro1");   
  }
  else
  {
    delay((period*1000) -(millis()-time_0));
  }
}
void temperatura_NTC()
{
  sensorValue = analogRead(sensorTemperature);   
  Serial.println(sensorValue);
}
void pulso(){
}
