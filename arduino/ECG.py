import serial
import time

# 시리얼 포트 설정 (포트 번호를 적절하게 변경하세요)
port = 'COM4'  # 적절한 포트로 변경
baudrate = 9600

try:
    # 시리얼 포트 열기
    ser = serial.Serial(port, baudrate)

    # 데이터를 저장할 리스트 초기화
    ecg_data = []

    # 데이터 수집 시간 (초)
    collect_time = 10
    start_time = time.time()

    try:
        while time.time() - start_time < collect_time:
            if ser.in_waiting:
                # 시리얼 버퍼에서 한 줄 읽기
                line = ser.readline().decode('utf-8').strip()
                # 읽은 데이터를 정수형으로 변환하여 리스트에 추가
                ecg_data.append(int(line))
    except KeyboardInterrupt:
        print("Data collection interrupted.")
    finally:
        # 시리얼 포트 닫기
        ser.close()

    # 수집된 데이터 출력
    print(ecg_data)

except serial.SerialException as e:
    print(f"Could not open port {port}: {e}")
