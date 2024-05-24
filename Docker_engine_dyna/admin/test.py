import json
import os
import docker
import yaml
import shutil

def copy_and_rename_files(source_dir, destination_dir, file_mapping):
    for src_file, dest_file in file_mapping.items():
        src_path = os.path.join(source_dir, src_file)
        dest_path = os.path.join(destination_dir, dest_file)
        shutil.copy(src_path, dest_path)

def extract_info_from_json(json_data):
    try:
        data = json.loads(json_data)
        app_id = data["id"]
        in_info = [(item[f"namelistener{i}"], item[f"typelistener{i}"]) for i, item in enumerate(data["in"])]
        treat_info = [(item[f"nametreatment{i}"], item[f"typetreatment{i}"]) for i, item in enumerate(data["treat"])]
        out_info = [(item[f"namesender{i}"], item[f"typesender{i}"]) for i, item in enumerate(data["out"])]
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

def generate_docker_compose(app_id, app_info):
    docker_compose = {
        'version': '3',
        'networks': {
            'reseau': None
        },
        'services': {}
    }
    directory_name = app_id
    parent_directory = os.path.dirname(os.getcwd()) 
    for index in app_info:
        service_name = f'{app_id}_{index}'
        build_context = f"{parent_directory}/{directory_name}/{service_name}"
        network = "reseau"
        volumes = f"{parent_directory}/{directory_name}/logs:/app/logs"
        docker_compose['services'][service_name] = {
            'container_name': service_name,
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
    client = docker.from_env()
    app_id, in_info, treat_info, out_info = extract_info_from_json(json)
    parent_directory = os.path.dirname(os.getcwd())
    concat = in_info + treat_info + out_info
    for service in concat:
        service_name = f'{app_id}_{service[0]}'
        type = service[1]  
        build_context = f"{parent_directory}/{app_id}/{service_name}" 
        os.makedirs(build_context, exist_ok=True)
        dockerfile_path = os.path.join(build_context, 'dockerfile')
        generate_dockerfile(service_name, dockerfile_path)
        file_mapping = {
            f'{type}.txt': 'requirements.txt',
            f'{type}.py': f'{app_id}_{type}.py',
        }
        copy_and_rename_files(f'{os.getcwd()}/default_codes',build_context,file_mapping)
        if type.startswith("listener"):
            publish_topic = f'{app_id}/listener'
        elif type.startswith("encrypt"):
            publish_topic = f'{app_id}/encrypt'
            subscribe_topic = f'{app_id}/listener'
        else:
            subscribe_topic = f'{app_id}/encrypt'
        with open(f'{build_context}/{app_id}_{type}.py', "r") as file:
            file_content = file.read()
        new_file_content = file_content.replace("PUBLISH_TOPIC", publish_topic).replace("SUBSCRIBE_TOPIC", subscribe_topic)
        with open(f'{build_context}/{app_id}_{type}.py', "w") as file:
            file.write(new_file_content)        
        container = client.containers.run(
            image = "python:3.10-slim",
            name = service_name,
            working_dir = f"/{app_id}",
            volumes = {f"{build_context}/": {'bind': f"/{app_id}", 'mode': 'ro'}},
            detach=True,  
            network = 'docker_engine_dyna_reseau',
            command = f"sh -c 'pip install --no-cache-dir -r requirements.txt && python3 {app_id}_{type}.py'"   
        )
        print("Conteneur créé avec succès. ID:", container.id)

    name_list = [info[0] for info in concat]
    generate_docker_compose(app_id, name_list)

# Exemple de JSON
json_data = '''
{
    "id": "app11",
    "in": [
        {
            "namelistener0": "l0",
            "typelistener0": "listener"
        },
        {
            "namelistener1": "l1",
            "typelistener1": "listener_bluetooth"
        }
    ],
    "treat": [
        {
            "nametreatment0": "t0",
            "typetreatment0": "encrypt"
        }
    ],
    "out": [
        {
            "namesender0": "s0",
            "typesender0": "sender"
        }
    ]
}
'''

generate_docker_app(json_data)
