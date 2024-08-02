from PIL import Image
import torch
from torchvision import transforms
from torchvision.models import resnet50
import boto3
import datetime, json, os, uuid


model = None


def handler(event):

    
    bucket_name = 'onanadbucket'
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    image_download_begin = datetime.datetime.now()
    s3.download_file(bucket_name, 'goldfish.jpeg', 'goldfish.jpeg')
    image_download_end = datetime.datetime.now()
    #s3.download_file(bucket_name, 'imagenet_class_index.json', 'imagenet_class_index.json')
    
    class_idx = json.load(open('/app/imagenet_class_index.json', 'r'))
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]
    
    
    global model
    if not model:
        model_download_begin = datetime.datetime.now()
        #s3.download_file(bucket_name, 'resnet50.pth', 'resnet50.pth')
        model_download_end = datetime.datetime.now()
        
        model_process_begin = datetime.datetime.now()
        model = resnet50(pretrained=False)
        model.load_state_dict(torch.load('/app/resnet50.pth'))
        model.eval()
        model_process_end = datetime.datetime.now()
        
    else:
        model_download_begin = datetime.datetime.now()
        model_download_end = model_download_begin
        model_process_begin = datetime.datetime.now()
        model_process_end = model_process_begin
        
    process_begin = datetime.datetime.now()
    input_image = Image.open('goldfish.jpeg')
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model 
    output = model(input_batch)
    _, index = torch.max(output, 1)
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    prob = torch.nn.functional.softmax(output[0], dim=0)
    _, indices = torch.sort(output, descending = True)
    ret = idx2label[index]
    process_end = datetime.datetime.now()

    download_time = (image_download_end- image_download_begin) / datetime.timedelta(microseconds=1)
    model_download_time = (model_download_end - model_download_begin) / datetime.timedelta(microseconds=1)
    model_process_time = (model_process_end - model_process_begin) / datetime.timedelta(microseconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)
    
    return {
            'result': {'idx': index.item(), 'class': ret},
            'measurement': {
                'download_time': download_time + model_download_time,
                'compute_time': process_time + model_process_time,
                'model_time': model_process_time,
                'model_download_time': model_download_time
            }
             
        }
        
    
    
 
def main(params):
     
    return handler({})
