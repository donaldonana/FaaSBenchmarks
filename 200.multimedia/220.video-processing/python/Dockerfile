FROM openwhisk/action-python-v3.9

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

RUN pip install numpy
RUN pip install boto3
RUN pip install Pillow==9.0.0
RUN python3 -m pip install opencv-Python

RUN pip install moviepy
RUN pip install imageio
