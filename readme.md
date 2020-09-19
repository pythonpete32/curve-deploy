# curve-deploy
Docker container for deploying and hacking on [curve.fi](curve.fi) DAO and contracts

<br>

##  ✅ Prerequisites
[docker](https://docs.docker.com/get-docker/) 

<br>

##  🏁 Quick Start

First pull the docker image

```
docker pull pythonpete32/curve-deploy:latest
```

Find the `IMAGE ID` by running 

```
docker images
```

then run launch a docker container with an interactive terminal

```
docker run -it <IMAGE_ID> /bin/bash
```

edit the seed in the python script for the deployment 
```
vim ./scripts/deploy-xdai.py
```

then run the associated bash script
```
./scripts/deploy-xdai.sh
```

<br>

##  💻 Manual

```
git clone https://github.com/pythonpete32/curve-deploy.git && cd ./curve-deploy
python3 -m venv venv

export WEB3_INFURA_PROJECT_ID=e22eadb98be944d18e48ab4bec7ecf3f
. ./venv/bin/activate
pip install -r requirements.txt

brownie run deploy-rinkeby --network rinkeby
```
<br>



If you have questions or need help please drop into the Aragon [Discord](https://discord.com/invite/remTh8w) support channel!