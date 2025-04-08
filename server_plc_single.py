import json
import time
import random
from opcua import Server

# AAS JSON 로드
with open("./writeAASAAS_test1.json", "r") as f:
    aas_data = json.load(f)

# OPC UA 서버 설정
server = Server()
url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(url)

name = "OPCUA_SERVER_TEST_AAS"
test_namespace = server.register_namespace(name)

node1 = server.get_objects_node()
node1_Param = node1.add_object(test_namespace, aas_data["id"])

# 특정 Property 노드 생성
# OperationData > temp 값 찾기
for submodel in aas_data["submodels"]:
    if submodel["id"] == "OperationData":
        for element in submodel.get("submodelElements", []):
            if element["idShort"] == "temp":
                temp_value = int(element["value"])  # 혹은 float() if needed
                temp_var = node1_Param.add_variable(test_namespace, "Temperature", temp_value)
                temp_var.set_writable()
                break

server.start()
print("🚀 OPC UA AAS Server Started")

try:
    while True:
        # 예: 온도 값을 무작위로 갱신
        new_temp = round(random.uniform(20.0, 30.0), 2)
        temp_var.set_value(new_temp)
        print(f"Updated Temperature: {new_temp}")
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    server.stop()
