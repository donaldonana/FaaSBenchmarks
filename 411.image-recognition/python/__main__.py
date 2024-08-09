from PIL import Image
import torch # type: ignore
from torchvision import transforms # type: ignore
from torchvision.models import resnet50, resnet18, resnet152 # type: ignore
import boto3
import datetime, json, os, uuid


model = None


def recognition(event):

    bucket_name = 'donaldbucket'
    aws_access_key_id = event["key"]
    aws_secret_access_key = event["access"]
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    # Image Downloading
    image_download_begin = datetime.datetime.now()
    s3.download_file(bucket_name, "15Mb.JPEG", "15Mb.JPEG")
    # download_size = os.path.getsize(event["file"])
    image_download_end = datetime.datetime.now()
    
    class_idx = json.load(open('/app/imagenet_class_index.json', 'r'))
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]
    
    
    global model
    if not model:
        
        model_process_begin = datetime.datetime.now()
        model = resnet18(pretrained=False)
        model.load_state_dict(torch.load('/app/resnet18.pth'))
        model.eval()
        model_process_end = datetime.datetime.now()
        
    else:
        model_download_begin = datetime.datetime.now()
        model_download_end = model_download_begin
        model_process_begin = datetime.datetime.now()
        model_process_end = model_process_begin
    
    model_size = os.path.getsize('/app/resnet18.pth')

        
    process_begin = datetime.datetime.now()
    input_image = Image.open('15Mb.JPEG')
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model 
    output = model(input_batch)
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    prob = torch.nn.functional.softmax(output[0], dim=0)
    max_prob, max_prob_index = torch.max(prob, dim=0)
    # _, indices = torch.sort(output, descending = True)
    ret = idx2label[max_prob_index]
    process_end = datetime.datetime.now()

    download_time = (image_download_end- image_download_begin) / datetime.timedelta(seconds=1)
    # model_download_time = (model_download_end - model_download_begin) / datetime.timedelta(microseconds=1)
    model_process_time = (model_process_end - model_process_begin) / datetime.timedelta(seconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(seconds=1)
    
    return {

            'idx': max_prob_index.item(),
            'class': ret, 
            'prob' : max_prob.item(),
            'compute_time': process_time + model_process_time,
            'model_time': model_process_time,
            # 'image'
            # 'model'
            'model_size' : model_size

            }
             
        
ResnetModel = {'resnet18' : resnet18, 'resnet50' : resnet50, 'resnet152' : resnet152}

    
def main(params):
     
    return recognition(params)
