import serial
import time
import requests
import json

# 시리얼 포트 설정
port = 'COM4'  # 실제 포트로 변경
baudrate = 9600
api_url = "https://your-api-endpoint.com/AI_MODEL"  # AI 모델 엔드포인트 URL

# 시리얼 포트 열기
ser = serial.Serial(port, baudrate)

# 데이터 전송 주기 (초)
send_interval = 1  # 1초마다 데이터 전송
buffer_size = 10  # 주기마다 보낼 데이터 개수

# 초기화
ecg_data = []
last_send_time = time.time()

try:
    while True:
        if ser.in_waiting:
            # 시리얼 버퍼에서 한 줄 읽기
            line = ser.readline().decode('utf-8').strip()
            ecg_data.append(int(line))

            # 현재 시간
            current_time = time.time()

            # 일정 주기마다 데이터 전송
            if current_time - last_send_time >= send_interval:
                if len(ecg_data) >= buffer_size:
                    # 버퍼 크기만큼 데이터를 묶어서 전송
                    data_to_send = ecg_data[:buffer_size]
                    ecg_data = ecg_data[buffer_size:]

                    # 데이터 전송
                    response = requests.post(api_url, json={'ecg_data': data_to_send})
                    if response.status_code == 200:
                        print("Data sent successfully")
                    else:
                        print(f"Failed to send data: {response.status_code}")

                    # 마지막 전송 시간 갱신
                    last_send_time = current_time

except KeyboardInterrupt:
    print("Data collection interrupted.")
finally:
    # 시리얼 포트 닫기
    ser.close()
