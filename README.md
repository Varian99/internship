# Multi protocol multi application gateway:

My intership project of a multi protocol multi application gateway, for my first year of master done in collaboration with Ugo Réolon.
This project is coded in Python and is using the Flask Python Framework for the web part.
It is using Docker containers to work, working firstly with docker-compose and dockerfiles, but we haven't fully made their implementation in Python to create and manage them.

## Contents

1. [Installation](#installation)
2. [Cloning the project](#cloning-the-project)
3. [Fonctionnalities](#fonctionnalities)
4. [Authors](#authors)
5. [Acknowledgment](#acknowledgment)

## Installation

This project is supposed to work on QEMU with a Debian image, but it is not absolutely needed, it can work on any VM or distribution with Docker working properly.
In this section I will cover on how to install Docker, using the official documentation.
If you want more information on QEMU you can read the official documentation, or in my intership report where I studied the important aspects of QEMU for the project.
Here are the commands you need to run to install Docker, using the apt repository.

First we need to set up Docker's apt repository.
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
```
Replace Debian with the name of your own distribution (example ubuntu).
```bash
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

```
Replace Debian with the name of your own distribution
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
Now we can install Docker
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Verify that Docker is properly installed and working with the hello-world image. 
```bash
sudo docker run hello-world
```
If you don't want to have to use sudo for every command related to Docker in the future, you can run this command:
```bash
sudo usermod -aG docker toto
```
## Cloning the project
Now that Docker is installed, you can clone this project.
With Git installed on your machine, you need to run this command inside the folder you want the project to be.
```bash
git clone https://github.com/Varian99/stage.git
```
## Fonctionnalities

You now have access to the project and you can directly test our features.
In the folder docker_engine folder, you have access to our first tests of the project using different containers to pass and treat information.
You can test them by entering in the folder and run:
```bash
docker-compose -f docker-compose-mqtt.yaml up -d
docker-compose -f {name of the docker compose of the application you want to test} up -d
```
You have access to logs folder inside the apps folder allowing you to see the data traveling, sadly the web part has been changed and you can't test the web part with mongoDB.
Don't forget to use the same commands as earlier, replacing up -d with down.

Before going into the dynamic part of the project, go inside Web_service and run:
```bash
docker compose up -d
```
Now you can go inside the Docker_engine_dyna being the part we did most of our work, you can test some of the apps we made here, they were created dynamically using templates of codes I made.
These templates and the code of this is inside the folder code and is using data.json as a parameter for the creation, implemented in the web part for the creation of the json.
You can access the website using the address your_ip_address:5000, and try to create your own json with the protocols etc.

## Future development

Some work will have to be done in the future to make this gateway such as:

Manage apps, being able to manage apps from the website and their containers, basically what we are doing with docker-compose but now in Python. Ugo has worked on the container creation 
in Python further than me and can print their logs in the website but it is not fully working yet with the protocols which are also not working properly and we can't test them. 

The container statistics needs to be implemented to do some statistics on how many communication you have inside a MQTT queue for example.

## Authors

Bertrand Hugo

Réolon Ugo

## Acknowledgment
Dauda Abdulkadir

Nolot Florent

Flauzac Olivier
