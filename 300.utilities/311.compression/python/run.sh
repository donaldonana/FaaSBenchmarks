#!/bin/bash
sudo docker build -t python3action:comp .
sudo docker tag python3action:comp onanad/python3action:comp
sudo docker push onanad/python3action:comp
wsk action update comp --docker onanad/python3action:proc __main__.py
wsk action invoke comp --result
wskdeploy -m manifest.yaml
