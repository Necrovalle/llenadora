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
#define sOF 9

//Nota.- Las señales seran 'A' para cargar A, 'a' par descargar A
//       'X' para cerrar A, 'B' para cargar B, 'b' para descargar 
//       B, 'Y' para cerrar B, paramandar al maestro la señal de
//       activacion es de '1' y un '0' para apagar, envia una F
//       para apagar el sistema completo.

char    ENT;  //lectura de comando del maestro por puerto serie
boolean ACT;  //Estado del sitema activo/inactivo
boolean END;  //Bandera de envio de apagado total
int     Td;   //Tiempo de espera de rebote e inductivos [ms]

void setup() {
  Serial.begin(9600);
  pinMode(A, OUTPUT); 
  pinMode(a, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(pON, INPUT);
  pinMode(pOF, INPUT);
  pinMode(sOF, INPUT);
  digitalWrite(A, HIGH);
  digitalWrite(a, HIGH);
  digitalWrite(B, HIGH);
  digitalWrite(b, HIGH);
  digitalWrite(13, HIGH);
  ACT = false;
  END = false;
  Td = 100;
  delay(800);
  digitalWrite(13, LOW);
  
}

void loop() {
  if (!digitalRead(pON)){
    if (!ACT){
      delay(Td);
      if (!digitalRead(pON)){
        Serial.print('1');
        ACT = true; 
      }
    }
  }

  if (!digitalRead(pOF)){
    if (ACT){
      delay(Td);
      if (!digitalRead(pOF)){
        Serial.print('0');
        ACT = false;
        END = false;
      }
    }
  }

  if (!digitalRead(sOF)){
    if (END == false){
      delay(Td);
      if (!digitalRead(sOF)){
        digitalWrite(A, HIGH);
        digitalWrite(a, HIGH);
        digitalWrite(B, HIGH);
        digitalWrite(b, HIGH);
        ACT = false;
        Serial.print('0');
        delay(1000);
        END = true;
        Serial.print('F');
      }
    }
  }
  
  //Lectura de ordenes del maestro
  if (Serial.available() > 0){
    ENT = Serial.read();
    switch (ENT){
      case 'A':
        digitalWrite(A, LOW);
        digitalWrite(a, HIGH);
        break;
      case 'a':
        digitalWrite(A, HIGH);
        digitalWrite(a, LOW);
        break;
      case 'X':
        digitalWrite(A, HIGH);
        digitalWrite(a, HIGH);
        break;
      case 'B':
        digitalWrite(B, LOW);
        digitalWrite(b, HIGH);
        break;
      case 'b':
        digitalWrite(B, HIGH);
        digitalWrite(b, LOW);
        break;
      case 'Y':
        digitalWrite(B, HIGH);
        digitalWrite(b, HIGH);
        break;
      default:
        Serial.print(ENT);
        digitalWrite(13, HIGH);
        break;
    }
  }
}

//************************************************* FIN  DE CODIGO
