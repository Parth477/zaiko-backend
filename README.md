# zaiko-backend


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.


### Setting up the environment locally.

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [OS X](https://docs.docker.com/docker-for-mac/install/)
* [Linux](https://docs.docker.com/engine/install/ubuntu/)

**Use docker compose build to build docker images**
```
make local_build 
```

**Stop old docker images**
```
sudo docker stop $(sudo docker ps -aq)
```

**Use docker up to bring up the setup.**
```
make local_up
```
**Create new migration file**
```
make web_shell
python3 manage.py makemigrations
```

