//****************************************************************
//* Emulador de sistema de llenadora
//****************************************************************

//Canales digitales de control de valvula
//Linea A
#define A 3
#define a 4
//linea B
#define B 5
#define b 6

//Nota.- Las señales seran 'A' para cargar A, 'a' par descargar A
//       'X' para cerrar A, 'B' para cargar B, 'b' para descargar 
//       B, 'Y' para cerrar B.

char ENT;

void setup() {
  Serial.begin(9600);
  pinMode(A, OUTPUT); 
  pinMode(a, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(A, LOW);
  digitalWrite(a, LOW);
  digitalWrite(B, LOW);
  digitalWrite(b, LOW);
  digitalWrite(13, HIGH);
  delay(1500);
  digitalWrite(13, LOW);
}

void loop() {
  if (Serial.available() > 0){
    ENT = Serial.read();
    switch (ENT){
      case 'A':
        digitalWrite(A, HIGH);
        digitalWrite(a, LOW);
        break;
      case 'a':
        digitalWrite(A, LOW);
        digitalWrite(a, HIGH);
        break;
      case 'X':
        digitalWrite(A, LOW);
        digitalWrite(a, LOW);
        break;
      case 'B':
        digitalWrite(B, HIGH);
        digitalWrite(b, LOW);
        break;
      case 'b':
        digitalWrite(B, LOW);
        digitalWrite(b, HIGH);
        break;
      case 'Y':
        digitalWrite(B, LOW);
        digitalWrite(b, LOW);
        break;
      default:
        Serial.print(ENT);
        digitalWrite(13, HIGH);
        break;
    }
  }
}

//************************************************* FIN  DE CODIGO
