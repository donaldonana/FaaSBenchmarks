#!/bin/bash
sudo docker build -t action-python-v3.9:html .
sudo docker tag action-python-v3.9:html onanad/action-python-v3.9:html
sudo docker push onanad/action-python-v3.9:html
wsk action update html --docker onanad/action-python-v3.9:html __main__.py
wsk action invoke html --result
#wskdeploy -m manifest.yaml
