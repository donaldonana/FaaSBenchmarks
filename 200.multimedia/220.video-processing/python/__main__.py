import os
from os import path
import numpy
import boto3
import cv2
import imageio
import datetime
import subprocess
from PIL import Image
from moviepy.editor import VideoFileClip



def video_to_gif_moviepy(input_video_path, output_gif_path, start_time=None, end_time=None):
    # Load the video
    clip = VideoFileClip(input_video_path)
    
    # Trim the video if start_time and end_time are provided
    if start_time and end_time:
        clip = clip.subclip()
    
    # Write the GIF file
    clip.write_gif(output_gif_path)
    

def video_to_gif_imageio(input_video_path, output_gif_path):
    # Load the video
    reader = imageio.get_reader(input_video_path)
    fps = reader.get_meta_data()['fps']
    
    # Write the GIF file
    writer = imageio.get_writer(output_gif_path, fps=fps)
    for frame in reader:
        writer.append_data(frame)
    writer.close()
    

def video_to_gif_opencv(input_video_path, output_gif_path):
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert the frame to RGB (PIL uses RGB instead of BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Append frame to the list
        frames.append(Image.fromarray(frame))

    cap.release()

    # Save frames as a GIF
    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0)
    


def video_to_gif_ffmpeg(input_video_path, output_gif_path):

    args = ["-i", input_video_path,
        "-vf",
        "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "-loop", "0",
        output_gif_path]
        
    ret = subprocess.run(["ffmpeg", '-y'] + args,
            #subprocess might inherit Lambda's input for some reason
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if ret.returncode != 0:
        print('Invocation of ffmpeg failed!')
        print('Out: ', ret.stdout.decode('utf-8'))
        raise RuntimeError()
        
    


def handler(args):

     # Connexion to Remote Storage
    bucket_name = 'donaldbucket'
    aws_access_key_id = args["key"]
    aws_secret_access_key = args["access"]
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    # Image Downloading
    download_begin = datetime.datetime.now()
    s3.download_file(bucket_name, args["file"], args["file"])
    download_size = os.path.getsize(args["file"])
    download_end = datetime.datetime.now()
    
    # Video to Gif Transformation
    process_begin = datetime.datetime.now()
    # out = biblio[args["bib"]](args["file"], args["width"], args["hight"])
    process_end = datetime.datetime.now()

    # out_size = os.path.getsize(out)
    
    # Gif Uploading
    upload_begin = datetime.datetime.now()
    # s3.upload_file(out, bucket_name, out)
    upload_end = datetime.datetime.now()
    
    download_time = (download_end - download_begin) / datetime.timedelta(seconds=1)
    upload_time = (upload_end - upload_begin) / datetime.timedelta(seconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(seconds=1)
    
    return {      
            'download_time': download_time,
            'download_size': download_size,
            'upload_time': upload_time,
            # 'upload_size': out_size,
            'compute_time': process_time,
            'library' : args["bib"],
            'image' : args["file"]
    }


def main(args):
    
    # Apply Resize Operation 
    result = handler({

        "file"  : args.get("file", '1Mb.avi'),
        "bib"   : args.get("bib", "pillow"),
        "key"   : args.get("key"),
        "access": args.get("access")

    })

    return {"body": result}
