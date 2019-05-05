FROM codercom/code-server:latest

EXPOSE 8443

VOLUME [ "${PWD}:/root/project" ]

RUN mkdir /code
RUN sudo apt-get update
# 1. Create a fonts, downloads and assets directory for the container.
# 2. Install `git` for SCM, `make` for `curl`, `curl` for downloading files, `unzip` for ZIP files and `fontconfig` for managing fonts.
# 3. This is a simpler version of `nvm`, called `n`, that installs the LTS version of node.
RUN sudo apt install git make curl unzip fontconfig -y
