import yaml
import os
import extract

def generate_dockerfile(listener_script,dockerfile_path):
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

def generate_txt(list_package,txt_path):
    with open(txt_path, "w") as requirements_file:
        for package in list_package:
            requirements_file.write(package + "\n")

def generate_docker_compose(app_info):
    docker_compose = {
        'version': '3',
        'networks': {
            'reseau': None
        },
        'services': {}
    }
    directory_name = app_info[0]
    for service_name in app_info[1:]:
        build_context = f"./{directory_name}/{service_name}"
        dockerfile = "dockerfile"
        network = "reseau"
        volumes = f"./{directory_name}/logs:/app/logs"
        os.makedirs(build_context, exist_ok=True)
        dockerfile_path = os.path.join(build_context, dockerfile)
        txt_path = os.path.join(build_context, "requirements.txt")
        generate_dockerfile(service_name,dockerfile_path)
        generate_txt(["paho-mqtt==2.0.0"],txt_path)
        docker_compose['services'][service_name] = {
            'build': {
                'context': build_context,
                'dockerfile': 'dockerfile'
            },
            'networks': [network],
            'volumes': [volumes]
        }


    file_path = os.path.join(os.getcwd(), f"docker-compose-{directory_name}.yaml")
    with open(file_path, 'w') as file:
        yaml.dump(docker_compose, file)
    print("docker-compose.yaml a été créé avec succès.")

def main():
    app_info_list = extract.extract_app_info_from_json("data.json")
    for app_info in app_info_list:
        directory_name = app_info[0]
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            generate_docker_compose(app_info)
        else:
            print(f"Une application du même nom existe déjà.")
            return
   
if __name__ == "__main__":
    main()