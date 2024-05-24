import docker
import json
import os.path

#Path to update !! Put the absolute path to docker-engine repertory
path_docker_engine = "/home/toto/stage/Docker-engine_dyna/"

def parse_json_for_containers(appName):

    json_file = f"/app/configApps/{appName}.json"
    with open(json_file, 'r') as f:
        app = json.load(f)
        app_id = app['id']
        in_names = [app["in"][i][f"nameListener{i}"] for i in range(len(app["in"]))]
        treat_names = [app["treat"][i][f"nameTreatment{i}"] for i in range(len(app["treat"]))]
        out_names = [app["out"][i][f"nameSender{i}"] for i in range(len(app["out"]))]

        app_folder = f"/app/appContainer/{app_id}"

        try:
            if not os.path.exists(app_folder):
                raise FileNotFoundError
        except FileNotFoundError:
            return f'Error 10 : directory "/app/appContainer/{app_id}" not found'
        
        for listener_container_name in in_names:
            response = create_and_start_listener_container(app_id,listener_container_name)
            if response != 0: 
                return response
 
        for treatment_container_name in treat_names:
            response = create_and_start_treatment_container(app_id,treatment_container_name)
            if response != 0:
                return response
        
        for sender_container_name in out_names:
            response = create_and_start_sender_container(app_id,sender_container_name)
            if response != 0:
                return response
    return 0


def create_and_start_listener_container(app_id,listener_container_name):
    try:
        # Create client docker
        client = docker.from_env()
        # Listener container image
        base_image = "python:3.10:slim"

        # Work directory of the container
        workdir = f"/{app_id}"

        # Path in the container
        requirements_container = f"requirements-{app_id}.txt"
        listener_container = f"{listener_container_name}/{listener_container_name}.py"

        # Create and launch listener container
        container = client.containers.run(
            image=base_image,
            working_dir=workdir,
            name=f"{app_id}-{listener_container_name}",
            volumes={f"{path_docker_engine}{app_id}": {'bind': f"/{app_id}", 'mode': 'ro'}},
            network= "docker-engine_my_network",
            command= f"sh -c 'pip install -r {requirements_container} && python3 {listener_container}'",
            detach=True
        )
    
    except docker.errors.ImageNotFound as e:
        print("Error Listener : Container image not found.")
        return f"11 : {e}"
    except docker.errors.APIError as e:
        print("Error Listener: Error with API Docker.")
        return f"12 : {e}"
    except docker.errors.ContainerError as e:
        print("Error Listener: During container execution.")
        return f"13 : {e}"
    except Exception as e:
        print("Error Listener: Other error")
        return f"19 : {e}"
    
    return 0

def create_and_start_treatment_container(app_id,treatment_container_name):
    
    try:
        client = docker.from_env()

        base_image = "python:3.10-slim"

        workdir = f"/{app_id}"

        requirements_container = f"requirements-{app_id}.txt"
        treatment_container = f"{treatment_container_name}/{treatment_container_name}.py"

        container = client.containers.run(
            image=base_image,
            working_dir=workdir,
            name=f"{app_id}-{treatment_container_name}",
            volumes={f"{path_docker_engine}{app_id}": {'bind': f"/{app_id}", 'mode': 'ro'}},
            network= "docker-engine_my_network",
            command= f"sh -c 'pip install -r {requirements_container} && python3 {treatment_container}'",
            detach=True
        )

    except docker.errors.ImageNotFound as e:
        print("Error Treatment : Container image not found.")
        return f"21 : {e}"
    except docker.errors.APIError as e:
        print("Error Treatment: Error with API Docker.")
        return f"22 : {e}"
    except docker.errors.ContainerError as e:
        print("Error Treatment: During container execution.")
        return f"23 : {e}"
    except Exception as e:
        print("Error Treatment: Other error")
        return f"29 : {e}"
    
    return 0

        
def create_and_start_sender_container(app_id,sender_container_name):
    try:
        client = docker.from_env()

        base_image = "python:3.10-slim"

        workdir = f"/{app_id}"

        requirements_container = f"requirements-{app_id}.txt"
        sender_container = f"{sender_container_name}/{sender_container_name}.py"

        container = client.containers.run(
            image=base_image,
            working_dir=workdir,
            name=f"{app_id}-{sender_container_name}",
            volumes={f"{path_docker_engine}{app_id}": {'bind': f"/{app_id}", 'mode': 'ro'}},
            network= "docker-engine_my_network",
            command= f"sh -c 'pip install -r {requirements_container} && python3 {sender_container}'",
            detach=True
        )

    except docker.errors.ImageNotFound as e:
        print("Error Sender: Container image not found.")
        return f"31 : {e}"
    except docker.errors.APIError as e:
        print("Error Sender: Error with API Docker.")
        return f"32 : {e}"
    except docker.errors.ContainerError as e:
        print("Error Sender: During container execution.")
        return f"33 : {e}"
    except Exception as e:
        print("Error Sender: Other error")
        return f"39 : {e}"
    
    return 0