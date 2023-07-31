import time
import paho.mqtt.client as mqtt
import serial

port = serial.Serial("/dev/ttyACM0", "9600", timeout=None)

broker_address = "210.119.12.59"  # MQTT 브로커의 주소

client = mqtt.Client("IOT59")  # 클라이언트 인스턴스 생성
client.connect(broker_address)  # MQTT 브로커에 연결


# client.publish(topic, _value)  # 토픽에 메시지 게시


# MQTT 클라이언트 객체 생성
client = mqtt.Client()

# MQTT 브로커에 연결
client.connect(broker_address)

# 보낼 토픽ㅡㅡ
topic01 = "temp" # 온도
topic02 = "humid" # 습도
topic03 = "gas" # 가스
topic04 = "flame" # 화재

# 보낼 값
n = 0

while True:
    data = port.readline().decode('utf-8').rstrip() 
    print(data)
    temp, humid, gas, flame = data.split(',')
    
    client.publish(topic01, temp)
    client.publish(topic02, humid)
    client.publish(topic03, gas)
    client.publish(topic04, flame)
    
    # 1초 대기
    time.sleep(1)

