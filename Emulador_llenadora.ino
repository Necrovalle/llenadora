//****************************************************************
//* Firmware de sistema de llenadora
//****************************************************************

//Canales digitales de control de valvula
//Linea A
#define A 3
#define a 4
//linea B
#define B 5
#define b 6
//Botones de accion
#define pON 7
#define pOF 8

//Nota.- Las señales seran 'A' para cargar A, 'a' par descargar A
//       'X' para cerrar A, 'B' para cargar B, 'b' para descargar 
//       B, 'Y' para cerrar B, paramandar al maestro la señal de
//       activacion es de '1' y un '0' para apagar

char    ENT;  //lectura de comando del maestro por puerto serie
boolean ACT;  //Estado del sitema activo/inactivo 

void setup() {
  Serial.begin(9600);
  pinMode(A, OUTPUT); 
  pinMode(a, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(pON, INPUT);
  pinMode(pOF, INPUT);
  digitalWrite(A, LOW);
  digitalWrite(a, LOW);
  digitalWrite(B, LOW);
  digitalWrite(b, LOW);
  digitalWrite(13, HIGH);
  ACT = false;
  delay(800);
  digitalWrite(13, LOW);
  
}

void loop() {
  if (digitalRead(pON)){
    if (!ACT){
      Serial.print('1');
      ACT = true;
    }
  }

  if (digitalRead(pOF)){
    if (ACT){
      Serial.print('0');
      ACT = false;
    }
  }
  
  //Lectura de ordenes del maestro
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

/************************************************* FIN  DE CODIGO
