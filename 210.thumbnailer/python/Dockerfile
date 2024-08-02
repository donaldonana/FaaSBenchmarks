FROM openwhisk/action-python-v3.9

 
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install boto3
RUN pip install Pillow==9.0.0
# RUN apt-get install libmagickwand-dev
RUN pip install Wand
RUN pip install pygame
RUN python3 -m pip install opencv-Python
RUN pip install psutil

