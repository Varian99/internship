import os
from flask import Flask, request
import docker
import yaml
import json

app = Flask(__name__)

client = docker.from_env()

# def extract_app_info_from_json(data):
#     app_info_list = []
#     sublist = []
#     app_id = data['id']
#     sublist.append(data['id'])
#     sublist.append(f"{data['in']['nameListener']}_{app_id}")
#     for name in data['treat'].values():
#         sublist.append(f"{name}_{app_id}")
#     sublist.append(f"{data['out']['nameSender']}_{app_id}")
#     app_info_list.append(sublist)
#     return app_info_list

def extract_info_from_json(json_data):
    try:
        data = json.loads(json_data)
        app_id = data["id"]
        in_info = [(item[f"namelistener{i}"], item[f"pubtoplistener{i}"]) for i, item in enumerate(data["in"])]
        treat_info = [(item[f"nametreatment{i}"], item[f"pubtoptreatment{i}"]) for i, item in enumerate(data["treat"])]
        out_info = [(item["namesender"],) for item in data["out"]]
        return app_id, in_info, treat_info, out_info
    except Exception as e:
        print(f"Error extracting information from JSON: {e}")
        return None

def generate_dockerfile(listener_script, dockerfile_path):
    dockerfile_content = f'''\
FROM python:3.10-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "{listener_script}.py"]
'''
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

def generate_txt(list_package, txt_path):
    with open(txt_path, "w") as requirements_file:
        for package in list_package:
            requirements_file.write(package + "\n")

def generate_docker_compose(app_id, in_info, treat_info, out_info):
    docker_compose = {
        'version': '3',
        'networks': {
            'reseau': None
        },
        'services': {}
    }
    directory_name = app_id
    parent_directory = os.path.dirname(os.getcwd()) 
    for service_name in in_info:
        build_context = f"{parent_directory}/{directory_name}/{service_name}"
        dockerfile = "dockerfile"
        network = "reseau"
        volumes = f"{parent_directory}/{directory_name}/logs:/app/logs"
        os.makedirs(build_context, exist_ok=True)
        dockerfile_path = os.path.join(build_context, dockerfile)
        txt_path = os.path.join(build_context, "requirements.txt")
        generate_dockerfile(service_name, dockerfile_path)
        generate_txt(["paho-mqtt==2.0.0"], txt_path)
        docker_compose['services'][service_name] = {
            'build': {
                'context': build_context,
                'dockerfile': 'dockerfile'
            },
            'networks': [network],
            'volumes': [volumes]
        }

    file_path = os.path.join(parent_directory, f"docker-compose-{directory_name}.yaml")
    with open(file_path, 'w') as file:
        yaml.dump(docker_compose, file)
    print("docker-compose.yaml a été créé avec succès.")


def generate_docker_app(json):
    app_id, in_info, treat_info, out_info = extract_info_from_json(json)
    parent_directory = os.path.dirname(os.getcwd())
    concat = in_info + treat_info
    for service in concat:
        service_name = service[0] 
        publish_topic = service[1]  
        build_context = f"{parent_directory}/{app_id}/{service_name}" 
        os.makedirs(build_context, exist_ok=True)
        dockerfile_path = os.path.join(build_context, 'dockerfile')
        txt_path = os.path.join(build_context, "requirements.txt")
        generate_dockerfile(service_name, dockerfile_path)
        generate_txt(["paho-mqtt==2.0.0"], txt_path)
    for service in out_info:
        service_name = service[0] 
        publish_topic = service[1]  
        build_context = f"{parent_directory}/{app_id}/{service_name}" 
        os.makedirs(build_context, exist_ok=True)
        dockerfile_path = os.path.join(build_context, 'dockerfile')
        txt_path = os.path.join(build_context, "requirements.txt")
        generate_dockerfile(service_name, dockerfile_path)
        generate_txt(["paho-mqtt==2.0.0"], txt_path)
    generate_docker_compose(app_id, in_info, treat_info, out_info)


@app.route('/add_app', methods=['POST'])
def create_containers():
    json_data = request.json
    generate_docker_app(json_data)
    return "Conteneurs créés avec succès" 


if __name__ == '__main__':
    app.run(debug=True)
