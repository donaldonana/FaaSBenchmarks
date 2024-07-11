#!/bin/bash
sudo docker build -t action-python-v3.9:thumb .
sudo docker tag action-python-v3.9:thumb onanad/action-python-v3.9:thumb
sudo docker push onanad/action-python-v3.9:thumb
wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py
wsk action invoke thumb --param bib pillow --result  --param bib 'pillow'
# wskdeploy -m manifest.yaml

