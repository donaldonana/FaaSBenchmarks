#!/bin/bash
sudo docker build -t action-python-v3.9:pagerank .
sudo docker tag action-python-v3.9:pagerank onanad/action-python-v3.9:pagerank
sudo docker push onanad/action-python-v3.9:pagerank
wsk action update pagerank --docker onanad/action-python-v3.9:pagerank __main__.py
wsk action invoke pagerank --result --param size 10
wskdeploy -m manifest.yaml

