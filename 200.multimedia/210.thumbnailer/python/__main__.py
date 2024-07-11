import datetime
import os
import sys
import boto3
import psutil
 

def opencv_resize(path, w, h):

    import cv2

    img = cv2.imread(path)

    # resize image by specifying custom width and height
    resized = cv2.resize(img, (w, h))

    resize_image = "resize_image.jpg"

    cv2.imwrite(resize_image, resized)

    return resize_image


def pygame_resize(path, w, h):

    import pygame

    # Initialize Pygame
    pygame.init()

    # Load the image
    image = pygame.image.load(path)

    # Resize the image
    reduced_image = pygame.transform.scale(image, (w, h))

    resize_image = "resize_image.jpg"
    # Save the reduced image
    pygame.image.save(reduced_image, resize_image)

    # Quit Pygame
    pygame.quit()

    return resize_image

def wand_resize(path, w, h):

    from wand.image import Image

    # Load the image
    img = Image(filename = path)

    # Resize the image
    img.resize(w, h)

    # Save the reduced image
    resize_image = "resize_image.jpg"
    # Save the reduced image
    img.save(filename=resize_image)

    return resize_image

 
def pillow_resize(path, w, h):

    from PIL import Image
    
    # Load the image
    img = Image.open(path)

    # Resize the image
    img.thumbnail((w,h))

    resize_image = "resize_image.jpg"

    # Save the reduced image
    img.save(resize_image)
    
    return resize_image
       

def resize(args):
  
    # Connexion to Remote Storage
    bucket_name = 'onanadbucket'
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        
    # Image Downloading
    download_begin = datetime.datetime.now()
    s3.download_file(bucket_name, args["file"], args["file"])
    download_size = os.path.getsize("img.jpg")
    download_end = datetime.datetime.now()

    # Image Resizing
    process_begin = datetime.datetime.now()
    out = biblio[args["bib"]](args["file"], args["width"], args["hight"])
    process_end = datetime.datetime.now()
    out_size = os.path.getsize(out)
    
    # Image Uploading
    upload_begin = datetime.datetime.now()
    s3.upload_file(out, bucket_name, out)
    upload_end = datetime.datetime.now()

    download_time = (download_end - download_begin) / datetime.timedelta(seconds=1)
    upload_time = (upload_end - upload_begin) / datetime.timedelta(seconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(seconds=1)


    return {      
            'download_time': download_time,
            'download_size': download_size,
            'upload_time': upload_time,
            'upload_size': out_size,
            'compute_time': process_time
    }


biblio = {'opencv' : opencv_resize, 'pillow' : pillow_resize, 'wand' : wand_resize, 'pygame' : pygame_resize}

def main(args):

    # Defauft args
    hight = 60
    width = 60 
    file = 'img.jpg'
    bib = "pillow"

    # Getting the user args if exist
    if "width" in args:
        width = args["width"]
    if "hight" in args:
        hight = args["hight"]
    if "file" in args:
        file = args["file"]
    if "bib" in args:
        bib = args["bib"]

    # Apply Resize Operation
    resultat = resize({
        "width" : width,
        "hight" : hight,
        "file"  : file,
        "bib"   : bib
    })

    return (resultat)
    
 