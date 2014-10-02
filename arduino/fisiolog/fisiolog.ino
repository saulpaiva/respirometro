// Interface de controle da estação fisiológica
// Baseado na estação meterologica
// Centro de Tecnologia Academica - UFRGS
// http://cta.if.ufrgs.br - 

int sensorTemperature = 5;    
float sensorValue = 0; 
bool flag_test= false;
void setup() {
	Serial.begin(115200);
        delay(1000);
}

void loop() {
	if(flag_test == true){
		temperatura_NTC();
		delay(333);
	}
	if (Serial.available())
 	 {
    		switch (Serial.read())
    		{
		        case 't':
		         temperatura_NTC();
		        break;
			case 'p':
      			 pulso();
      			break;
                        case 'a': //Retirar 
                          flag_test = !(flag_test);
                        break;
		        default:
		       break;
		    }
		  }
}
void temperatura_NTC()
{
	sensorValue = analogRead(sensorTemperature);   
 	Serial.println(sensorValue);

}
void pulso(){
}
