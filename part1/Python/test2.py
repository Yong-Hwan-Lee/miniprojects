import time
import paho.mqtt.client as mqtt

broker_address = "210.119.12.59"  # MQTT 브로커의 주소

client = mqtt.Client("IOT59")  # 클라이언트 인스턴스 생성
client.connect(broker_address)  # MQTT 브로커에 연결

topic = "Campus"  # 메시지를 게시할 토픽
sensor_value = "센서 값"  # 보낼 센서 값

client.publish(topic, sensor_value)  # 토픽에 메시지 게시

client.disconnect()  # MQTT 브로커와의 연결 해제import time
import paho.mqtt.client as mqtt

# MQTT 브로커의 주소
broker_address = "210.119.12.59"

# MQTT 클라이언트 객체 생성
client = mqtt.Client()

# MQTT 브로커에 연결
client.connect(broker_address)

# 보낼 토픽ㅡㅡ
topic = "AATest"

# 보낼 값
n = 0

while True:
    # 메시지 전송
    client.publish(topic, str(n))
   
    # n 값 증가
    n += 1
    print(n)
    # 1초 대기
    time.sleep(1)