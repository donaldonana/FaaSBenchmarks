#!/bin/bash
sudo docker build -t python3action:proc .
sudo docker tag python3action:proc onanad/python3action:proc
sudo docker push onanad/python3action:proc
wsk action update proc --docker onanad/python3action:proc __main__.py
wsk action invoke proc --result
wskdeploy -m manifest.yaml

