#!/bin/bash
sudo docker build -t action-python-v3.9:mst .
sudo docker tag action-python-v3.9:mst onanad/action-python-v3.9:mst
sudo docker push onanad/action-python-v3.9:mst
wsk action update mst --docker onanad/action-python-v3.9:mst __main__.py
wsk action invoke mst --result --param size 10
wskdeploy -m manifest.yaml

