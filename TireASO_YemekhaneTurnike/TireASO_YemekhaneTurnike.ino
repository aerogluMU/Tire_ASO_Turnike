#include <MFRC522.h>
#include <SPI.h>

int RFID_PIN = 9;
int SS_PIN = 10;

MFRC522 rfid(SS_PIN, RFID_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {
  if(!rfid.PICC_IsNewCardPresent()){
    return;
  }
  if(!rfid.PICC_ReadCardSerial()){
    return;
  }
  for(int sayac=0;sayac<4;sayac++){
    Serial.print(rfid.uid.uidByte[sayac]);
  }
  Serial.println("");
  rfid.PICC_HaltA();
}
