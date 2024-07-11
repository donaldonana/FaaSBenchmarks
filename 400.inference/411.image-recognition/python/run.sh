#!/bin/bash
sudo docker build -t action-python-v3.9:imgrec .
sudo docker tag action-python-v3.9:imgrec onanad/action-python-v3.9:imgrec
sudo docker push onanad/action-python-v3.9:imgrec
wsk action update imgrec --timeout 300000 --memory 512 --docker onanad/action-python-v3.9:imgrec __main__.py
wsk action invoke imgrec --result
wskdeploy -m manifest.yaml
