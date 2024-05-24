import os

def delete_docker_compose(service_name):
    file_path = f"docker-compose-{service_name}.yaml"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Fichier {file_path} supprimé avec succès.")
    else:
        print(f"Le fichier {file_path} n'existe pas.")

    service_directory = f"./{service_name}"
    if os.path.exists(service_directory):
        for root, dirs, files in os.walk(service_directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(service_directory)
        print(f"Dossier {service_directory} supprimé avec succès.")
    else:
        print(f"Le dossier {service_directory} n'existe pas.")

    with open('config_mqtt.txt', 'r') as file:
        lines = file.readlines()
    updated_lines = [line for line in lines if not line.startswith(service_name)]
    with open('config_mqtt.txt', 'w') as file:
        file.writelines(updated_lines)

def main():
    service_name = input("Nom de la file : ")
    delete_docker_compose(service_name)

if __name__ == "__main__":
    main()