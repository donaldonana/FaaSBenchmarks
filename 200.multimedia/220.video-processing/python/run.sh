#!/bin/bash
docker build -t action-python-v3.9:proc .
docker tag action-python-v3.9:proc onanad/action-python-v3.9:proc
docker push onanad/action-python-v3.9:proc
wsk action update proc --docker onanad/action-python-v3.9:proc __main__.py --web true
wsk action invoke proc  --result  --param bib ffmpeg --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY --param file 1Mb.avi

