import yaml
import os

def generate_mosquitto_conf(port_number, data_dir, log_dir):
    conf_content = f"""\
listener {port_number}
protocol mqtt
persistence true
allow_anonymous true
persistence_location {data_dir}
log_dest file {log_dir}/mosquitto.logs
"""
    return conf_content

def generate_dockerfile(service_name):
    dockerfile_content = f"""\
FROM eclipse-mosquitto

WORKDIR /{service_name}

COPY config/mosquitto.conf /{service_name}/config/mosquitto.conf

VOLUME /{service_name}/data
VOLUME /{service_name}/logs

CMD ["mosquitto", "-c", "/{service_name}/config/mosquitto.conf"]
"""
    return dockerfile_content

def generate_docker_compose(service_name, port_number):

    service_directory = f"./{service_name}"
    os.makedirs(service_directory, exist_ok=True)

    subdirectories = ['logs', 'config', 'data']
    for subdir in subdirectories:
        subdir_path = os.path.join(service_directory, subdir)
        os.makedirs(subdir_path, exist_ok=True)

    dockerfile_content = generate_dockerfile(service_name)
    with open(os.path.join(service_directory, 'Dockerfile'), 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

    conf_content = generate_mosquitto_conf(port_number, f"/{service_name}/data/", f"/{service_name}/logs/")
    with open(os.path.join(service_directory, 'config', 'mosquitto.conf'), 'w') as conf_file:
        conf_file.write(conf_content)

    docker_compose = {
        'version': '3',
        'services': {
            service_name: {
                'container_name': service_name,
                'restart': 'always',
                'build': {
                    'context': f'./{service_name}',
                    'dockerfile': 'Dockerfile'
                },
                'ports': [f'{port_number}:{port_number}'],
                'networks': ['reseau'],
                'volumes': [
                    f'./{service_name}/config:/{service_name}/config',
                    f'./{service_name}/data:/{service_name}/data',
                    f'./{service_name}/logs:/{service_name}/logs'
                ]
            }
        },
        'networks': {
            'reseau': None
        }
    }

    file_path = f'docker-compose-{service_name}.yaml'
    with open(file_path, 'w') as file:
        yaml.dump(docker_compose, file)
    print(f"docker-compose-{service_name}.yaml a été créé avec succès.")
    with open('config_mqtt.txt', 'a') as file:
        file.write(f"{service_name} {port_number}\n")

def main():
    service_name = input("Nom du service : ")
    port_number = input("Numéro de port : ")
    generate_docker_compose(service_name, port_number)

if __name__ == "__main__":
    main()