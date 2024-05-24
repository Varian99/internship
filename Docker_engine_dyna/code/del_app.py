import os

def delete_docker_compose(directory_name):
    file_path = f"docker-compose-{directory_name}.yaml"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Fichier {file_path} supprimé avec succès.")
    else:
        print(f"Le fichier {file_path} n'existe pas.")

    service_directory = f"./{directory_name}"
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

def main():
    directory_name = input("Nom de l'application : ")
    delete_docker_compose(directory_name)

if __name__ == "__main__":
    main()