#!/bin/bash
sudo docker build -t action-python-v3.10:upload --network=host .
sudo docker tag action-python-v3.10:upload onanad/action-python-v3.10:upload
sudo docker push onanad/action-python-v3.10:upload
wsk action update upload --docker onanad/action-python-v3.10:upload __main__.py
wsk action invoke upload --result
#wskdeploy -m manifest.yaml
