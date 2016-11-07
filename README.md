# CHROnIC_Bus
##**Cisco Health Report & ONline Information Collector**
This is an application designed to interact with infrastructure components, and perform an online analysis of them.

*The Challenge* - It can be tedious to collect the data needed for routine health analysis. For example, the UCS Health Check requres a PowerShell script to be ran, which requires the UCS PowerTools to be installed, as well as a number of security requirements. This can be very complex for anyone who does not routinely use PowerShell.

*The Solution* - Create an application that will enable interaction with UCS from the cloud. This particular application has several microservices, including:

* Bus - Used as a basic HTTP-based message queue
* Collector - On-prem component used to exchange core information between on-prem infrastructure and the Portal. Consumes messages from the queue.
* Portal - Information Collection service and agent used to push tasks into the queue.
* TBD

Contributors - Josh Anderson, Chad Peterson, Loy Evans

This repo is for the following service:
Bus - This microservice to designed to accept and distribute jobs from a queue. Not designed to be an especially feature rich message bus, but created for a specific purpose - to asynchronously send/receive messages via HTTP REST API. This bus is designed to sit in a public infrastructure and be reachable from environments that sit behind a HTTP Proxy server, with limited outbound connectivity.

This repo includes the following resources:
**Repo Information**
* README.md
    * This document
* .gitignore
    * Standard gitignore file to prevent commiting unneeded or security risk files

**CICD Build Configuration**
* .drone.yml
    * CICD Build instructions for Drone Server
* drone_secrets_sample.yml
    * template for the secrets file that will be used to encrypt credentials
* Dockerfile
    * Docker build file for applicaiton container
* requirements.txt
    * pip installation requirements

**Application Files**
* app.py
    * This kicks off the application. This application listens and is delivered strictly as an API.
* test.py
    * Flask build test application. Used to validate API functionality for the build process.

# Installation

## Environment

* [Docker Container](#opt1)
* [Native Python](#opt2)

## Docker Installation<a name="opt1"></a>

**Prerequisites:**
The following components are required to locall run this container:
* [Docker](https://docs.docker.com/engine/installation/mac/)

**Get the container:**
The latest build of this project is available as a Docker image from Docker Hub:
```
docker pull joshand/chronic_bus:latest
```

**Run the application:**
```
docker run -d -p 5000:5000 --name Dockerfile joshand/chronic_hub:latest
```

**Use the API:**
[API Usage](#api) See below for API usage

## Local Python Installation<a name="opt2"></a>

**Prerequisites:**
The following components are required to locally run this project:
* [Python 3.5](http://docs.python-guide.org/en/latest/starting/install/osx/) - Install via homebrew recommended if on a Mac
* git - Part of the Xcode Command Line Tools
* [pip](https://pip.pypa.io/en/stable/installing/)
* [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

**Get the code:**
The latest build of this project is available on Github:
```
mkdir ~/chronic_bus
cd ~/chronic_bus
git clone https://github.com/joshand/CHROnIC_Bus
```

**Set up virtual environment and PIP:**
```
virtualenv chronic
source chronic/bin/activate
pip install -r requirements.txt
```

**Execute the app:**
```
python app.py
```

**Use the API:**
[API Usage](#api) See below for API usage

# API Usage<a name="api"></a>
**Note: This usage assumes you are executing on localhost**
```
* 127.0.0.1:5000/api/send/<channelid> POST
    {
        "coldata": "your data or message here",
        "status": "1",
        "webhook": "https://url_for_webhook"
    }
* 127.0.0.1:5000/api/get/<channelid>  GET
* 127.0.0.1:5000/api/send/<channelid> DELETE
* 127.0.0.1:5000/api/status/<taskid>  POST
    {
        "status": "2"
    }
* 127.0.0.1:5000/api/status/<taskid>  GET
```
