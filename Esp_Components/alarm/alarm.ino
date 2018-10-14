#define sensor A0


void setup ()
{
  Serial.begin(9600);
  pinMode (sensor, INPUT) ;
}

void loop (){
  Serial.println(analogRead(A0));
  delay(200);
}
