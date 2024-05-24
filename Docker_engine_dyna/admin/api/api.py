from flask import Flask, request, jsonify, redirect, url_for
import json
import os.path 
from container import parse_json_for_containers


app = Flask(__name__)

@app.route('/create-app', methods=['POST'])
def create_app():
    data = request.get_json()
    appName = data.get('appName')
    listenersName = data.get('listenersName')
    listenersProto = data.get('listenersProto')
    listenersProtoPort = data.get('listenersProtoPort')   
    treatmentsName = data.get('treatmentsName')
    sendersName = data.get('sendersName')
    response_create_json = create_json(appName,listenersName,listenersProto,listenersProtoPort,treatmentsName,sendersName)
   
    if response_create_json == 0:
        response_generate_app = generate_app(appName)
        if response_generate_app == 0:
            response_container = parse_json_for_containers(appName)
            return jsonify({
                'result': str(response_container)
            })
        else:
            return jsonify({
                'result': str(response_generate_app)
            })
    else:
        return jsonify({
            'result': str(response_create_json)
        })



def create_json(appName,listenersName,listenersProto,listenersProtoPort,treatmentsName,sendersName):
    
    json_data = {
        "id": appName,
        "in": [], 
        "treat": [],
        "out": []
    }

    # Générer la section "in"
    for i, (listener_name, listener_protocol, listener_port) in enumerate(zip(listenersName,listenersProto,listenersProtoPort)):
        json_data["in"].append({
            f"nameListener{i}": listener_name,
            f"protocolListener{i}": listener_protocol,
            f"portListener{i}": listener_port
        })

    # Générer la section "treat"
    for i, (treatment_name) in enumerate(zip(treatmentsName)):
        json_data["treat"].append({
            f"nameTreatment{i}": treatment_name,
        })

    # Générer la section "out"
    for i, sender_name in enumerate(sendersName):
        json_data["out"].append({
            f"nameSender{i}": sender_name,
        })

    filename = f"/app/configApps/{appName}.json"

    if os.path.exists(filename):
        print(f"Error : File '{filename}' already exist.")
        return f"Error 1 : File '{filename}' already exist."
    else:
        try:
            with open(filename, "w") as json_file:
                json.dump(json_data, json_file, indent=4)
                return 0
        except Exception as e:
            return f"Error 9 : {e}" 
    
def generate_app(appName):
    json_file = f"/app/configApps/{appName}.json"
    with open(json_file, 'r') as f:
        app = json.load(f)
        app_id = app['id']
        in_names = [app["in"][i][f"nameListener{i}"] for i in range(len(app["in"]))]
        treat_names = [app["treat"][i][f"nameTreatment{i}"] for i in range(len(app["treat"]))]
        out_names = [app["out"][i][f"nameSender{i}"] for i in range(len(app["out"]))]

        app_folder = f"/app/appContainer/{app_id}"

        if not os.path.exists(app_folder):
            try:
                os.makedirs(app_folder)
            except OSError as e:
                print(f"Error when create directory {e}")
                return f"Error 2 :{e}"
        else:
            print(f'Directory "/appContainer/{app_id}" already exist.')
            return f'Error 3 : Directory "/appContainer/{app_id}" already exist.'

        for filename in list(in_names) + list(treat_names)+ list(out_names):
            folder_path = f"{app_folder}/{filename}"
            os.makedirs(folder_path, exist_ok=True)

            # Create Python file
            with open(f"{folder_path}/{filename}.py", 'w') as py_file:
                py_file.write(
                    f"import time\n"
                    f"import paho.mqtt.client as mqtt\n\n"
                    f'mqtt_broker_host = "mosquitto"\n\n'
                    f'print("Start of script !!")\n'
                    f'time.sleep(30)\n'
                    f'print("End of script !!")'
                )

            #Create Dockerfiles
            with open(f"{folder_path}/Dockerfile", 'w') as dockerfile:
                dockerfile.write(
                    f"FROM arm32v7/python:3.11-slim-buster\n\n"
                    f"WORKDIR /{app_id}\n\n"
                    f"COPY ./{app_id}/requirements-{app_id}.txt /{app_id}/\n\n"
                    f"RUN pip install -r requirements-{app_id}.txt\n\n"
                    f"COPY ./{app_id}/{filename}/{filename}.py /{app_id}/{filename}/\n\n"
                    f'CMD ["python", "{filename}.py"]'
                )

        # Create requirements.txt
        with open(f"{app_folder}/requirements-{app_id}.txt", 'w') as req_file:
            req_file.write(f"paho-mqtt==2.0.0")

        #Create docker-compose.yml 
        with open(f"/app/appContainer/docker-compose-{app_id}.yml", 'w') as docker_compose:
            docker_compose.write(
                f"version: '3'\n"
                f"services:\n"
            )
            for filename in list(in_names) + list(treat_names)+ list(out_names):
                docker_compose.write(
                    f"  {app_id}-{filename}:\n"
                    f"    container_name: {app_id}-{filename}\n"
                    f"    build:\n"
                    f"      context: .\n"
                    f"      dockerfile: ./{app_id}/{filename}/Dockerfile\n"
                    f"    volumes:\n"
                    f"      - ./{app_id}/logs:/{app_id}/logs\n"
                    f"    networks:\n"
                    f"      - my_network\n\n"
                )
            
            docker_compose.write(
                f"networks:\n"
                f"  my_network:"
            )
    return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)