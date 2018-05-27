#define sensor A0


void setup ()
{
  Serial.begin(115200);
  pinMode (sensor, INPUT) ;
}

void loop (){
  Serial.println(analogRead(A0));
  delay(200);
}
