This repo is named after the Greek Titan.
This repo contains Jupyter notebooks, Kaggle competition submission related files etc.

Below are instructions to using a Docker container to run Jupyter notebooks

# Instructions

## Using docker

- docker pull jupyter/datascience-notebook
- docker run --rm --name jup -p 8888:8888 -v "C:\My Development\Projects\Helios\src\Jupyter":/home/jovyan jupyter/datascience-notebook
- Open browser to http://127.0.0.1:8888
