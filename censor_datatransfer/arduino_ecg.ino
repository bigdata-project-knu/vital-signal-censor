
// #include <Arduino.h>
#include <ESP8266WiFi.h> //와이파이 라이브러리
#include "FirebaseESP8266.h"  //파이어베이스 라이브러리

#define WIFI_SSID "your_ssid" //와이파이 이름
#define WIFI_PASSWORD "your_password" //와이파이 비밀번호
#define WIFI_LED 2 //와이파이 연결 상태를 알려주는 LED
 //파이어베이스 라이브러리
//서버 코드 없이 데이터베이스, 서버기능사용

FirebaseData firebaseData; //파이어베이스 데이터
FirebaseJsonArray sdata; //파이어베이스 JSON 배열



void setup() {
  
Serial.begin(9600); //시리얼 통신
pinMode(A0,INPUT); //아날로그 입력
WiFi.begin(WIFI_SSID, WIFI_PASSWORD); //와이파이 연결
while (WiFi.status() != WL_CONNECTED ) {
  delay(200); //와이파이 연결 대기
  Serial.print(".");  //와이파이 연결 중
} 
Serial.println(""); //와이파이 연결 완료
Seroal.println("WiFi connected"); //와이파이 연결 완료
Serial.println("IP address: "); //IP 주소
Serial.println(WiFi.localIP()); //로컬 IP 주소
Firebase.begin("your_project_id", "your_database_secret"); //파이어베이스 연결
delay(1000);
}

void loop() {
  for ( int i =0; i < 250; i++) {
    sdata.set('/["+String(i)+"]', //파이어베이스 데이터 경로
    analogRead(A0) //아날로그 입력값 저장
    ); //파이어베이스 데이터 저장
  }
  Firebase.setArray( //파이어베이스 데이터 전송
    firebaseData,//파이어베이스 데이터
   "/ecg",//파이어베이스 데이터 경로
   sdata); 
}
