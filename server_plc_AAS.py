import json
import time
import random
from opcua import Server, ua

# AAS JSON 로드
with open("./writeAASAAS_test1.json", "r") as f:
    aas_data = json.load(f)

# OPC UA 서버 설정
server = Server()
url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(url)

name = "OPCUA_SERVER_AAS_FULL"
test_namespace = server.register_namespace(name)

objects = server.get_objects_node()

# AAS 루트 노드 생성
test_aas_id = aas_data["assetAdministrationShells"][0]["id"]
aas_node = objects.add_object(test_namespace, test_aas_id)

# AAS 전체 등록
submodel_dict = {}
for submodel in aas_data["submodels"]:
    submodel_id = submodel["id"]
    submodel_node = aas_node.add_object(test_namespace, submodel_id)
    submodel_dict = {submodel_id} = submodel_node
    
    for element in submodel.get("submodelElements", []):
        id_short = element.get("idShort", "unknown")
        value = element.get("value", "")
        value_type = element.get("valueType", "xs:string")

        # 타입 매핑 처리
        if value_type == "xs:int":
            cast_val = int(value)
            var = submodel_node.add_variable(test_namespace, id_short, cast_val, ua.VariantType.Int32)
        elif value_type == "xs:float":
            cast_val = float(value)
            var = submodel_node.add_variable(test_namespace, id_short, cast_val, ua.VariantType.Float)
        elif value_type == "xs:string":
            var = submodel_node.add_variable(test_namespace, id_short, str(value), ua.VariantType.String)
        else:
            var = submodel_node.add_variable(test_namespace, id_short, str(value), ua.VariantType.String)

        var.set_writable()

        # temp라는 idShort에 대해 값 주기적 변경을 위해 저장
        if id_short == "temp":
            temp_var = var

# 서버 시작
server.start()
print("🚀 OPC UA AAS Server Started")

try:
    while True:
        # PLC 대체 데이터
        if temp_var:
            new_temp = random.randint(20, 30)
            temp_var.set_value(new_temp)
            print(f"🔥 Updated temp: {new_temp}")
        time.sleep(2)
except KeyboardInterrupt:
    print("🛑 서버 종료 중...")
finally:
    server.stop()