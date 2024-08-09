FROM openwhisk/action-python-v3.9

WORKDIR /app

RUN pip install numpy==1.22.0
RUN pip install torch==1.11.0
RUN pip install torchvision==0.12.0
RUN pip install boto3

COPY ./resnet50.pth /app
COPY ./resnet18.pth /app

COPY ./imagenet_class_index.json /app
