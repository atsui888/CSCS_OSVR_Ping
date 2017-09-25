//int iInput = 0;
byte LEDPin1 = 3;
byte LEDPin2 = 5;

void setup() {
  // no pinMode for analogWrite or it will fail
  //pinMode(LEDPin1, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  //sendDataToUSB();
  receiveDataFromUSB();
  delay(1000);
}

void sendDataToUSB () {
  Serial.println("Hello from Ardunio!!!"); // write a string
}


void receiveDataFromUSB() {
  if (Serial.available() > 0)
  {
    char inByte = Serial.read();

    switch (inByte) {
      case 0:
        break;
        
      case 1:
        break;

      case 3:
        AnalogSignal_Out_TypeD(); // Output 1, SUCCESS
        break;

      case 5:
        AnalogSignal_Out_TypeE(); // Output 2, FAILURE
        break;

      default:
        break;
    }
    inByte = 0;
  }
}

void AnalogSignal_Out_TypeA() {
  analogWrite(LEDPin1,0);
  delay(1000);
  for(int i=0;i<=255;i++){
    analogWrite(LEDPin1,i);
  }   
}

void AnalogSignal_Out_TypeB() {
  for (int i = 0; i <= 255; i++)
  {
    analogWrite(LEDPin1, i);
    delay(3);
    //delay(39);
  }
  for (int i = 255; i >= 0; i--)
  {
    analogWrite(LEDPin1, i);
    delay(3);
    //delay(39);
  }  
}

void AnalogSignal_Out_TypeC() {
  analogWrite(LEDPin1, 255);
  delay(100);
  analogWrite(LEDPin1, 0);
  delay(100);
  analogWrite(LEDPin1, 255);
  delay(100);
  analogWrite(LEDPin1, 0);   
}

void AnalogSignal_Out_TypeD() {
  analogWrite(LEDPin1,0);
  delay(10);  
  analogWrite(LEDPin1,255);  
  delay(10000);
  analogWrite(LEDPin1,0);    
}

void AnalogSignal_Out_TypeE() {
  analogWrite(LEDPin2,0);
  delay(10);  
  analogWrite(LEDPin2,255);  
  delay(10000);
  analogWrite(LEDPin2,0);    
}
