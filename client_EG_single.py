from opcua import Client
import time
import os

# ip.txt: OPC UA Server의 ip 주소
ip_file_path = "C:/Users/rund6/OneDrive/바탕 화면/ip.txt"

with open(ip_file_path, "r") as file:
    ip_address = file.readline().strip()

# OPC UA 서버 주소 생성
url = f"opc.tcp://{ip_address}:4840"
client = Client(url)
client.connect()

try:
    # 서버 구조에서 temp 노드 찾아놓기
    objects = client.get_objects_node()
    aas_node = objects.get_child(["2:test1"])  # AAS ID가 "test1"
    submodel_node = aas_node.get_child(["2:OperationData"])  # Submodel ID
    temp_node = submodel_node.get_child(["2:temp"])  # 변수 이름

    # 5번 주기적으로 temp 값 읽기
    cnt = 0
    while cnt <= 4:
        temp_value = temp_node.get_value()
        print(f"temp 값({cnt + 1}/5): {temp_value}")
        print("----------------------------")
        time.sleep(2)
        cnt += 1

finally:
    client.disconnect()
    print("🔌 클라이언트 연결 종료")