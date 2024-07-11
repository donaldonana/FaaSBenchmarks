#!/bin/bash
sudo docker build -t action-python-v3.9:bfs .
sudo docker tag action-python-v3.9:bfs onanad/action-python-v3.9:bfs
sudo docker push onanad/action-python-v3.9:mst
wsk action update bfs --docker onanad/action-python-v3.9:mst __main__.py
wsk action invoke bfs --result --param size 10
wskdeploy -m manifest.yaml

