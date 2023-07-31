import time
import paho.mqtt.client as mqtt
import serial

port = serial.Serial("/dev/ttyACM0", "9600", timeout=None)
port2 = serial.Serial("/dev/ttyACM1", "9600", timeout=None)

cmd='temp'
port.write(cmd.encode())
broker_address = "210.119.12.59"  # MQTT 브로커의 주소

client = mqtt.Client("IOT59")  # 클라이언트 인스턴스 생성
client.connect(broker_address)  # MQTT 브로커에 연결


flame = "Flame"  # 보낼 센서 값
gas = "Gas"
temp ="Temp"
humid="Humid"
light = "Light"
rain = "Rain"


# client.publish(topic, _value)  # 토픽에 메시지 게시

client.disconnect()  # MQTT 브로커와의 연결 해제import time
import paho.mqtt.client as mqtt

# MQTT 브로커의 주소
broker_address = "210.119.12.59"

# MQTT 클라이언트 객체 생성
client = mqtt.Client()

# MQTT 브로커에 연결
client.connect(broker_address)

# 보낼 토픽ㅡㅡ
# 보낼 값
n = 0

while True:
    # 메시지 전송


    # 조도센서
    data2 = port2.readline().decode('utf-8').rstrip()
    client.publish(light,data2)
    print(data2)

    # 빗물감지
    data2 = port2.readline().decode('utf-8').rstrip()
    client.publish(rain,data2)
    print(data2)

    # 습도
    data = port.readline().decode('utf-8').rstrip()
    client.publish(temp, data)
    print(data)
    
    # 온도
    data = port.readline().decode('utf-8').rstrip()
    client.publish(humid,data )
    print(data)

    # 가스
    data = port.readline().decode('utf-8').rstrip()
    client.publish(gas,data)
    print(data)
    # 화재
    data = port.readline().decode('utf-8').rstrip()
    client.publish(flame,data)
    print(data)


    # n 값 증가


  
    # 1초 대기
    time.sleep(1)