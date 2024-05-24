import os
import shutil

def dispatch_files(application_name):
    source_directory = f'{application_name}_data'
    file_names = os.listdir(source_directory)
    for file_name in file_names:
        source_file_path = os.path.join(source_directory, file_name)
        if os.path.isfile(source_file_path):
            base_name, extension = os.path.splitext(file_name)
            new_file_name = f"{base_name}_{application_name}{extension}"
            destination_directory = os.path.join(os.getcwd(), f'{application_name}/{base_name}_{application_name}')
            destination_file_path = os.path.join(destination_directory, new_file_name)
            shutil.move(source_file_path, destination_file_path)

def main():
    service_name = input("Nom de l'application : ")
    dispatch_files(service_name)

if __name__ == "__main__":
    main()
    