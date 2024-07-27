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
        
    


def handler(event):

    duration = 9
    bucket_name = 'onanadbucket'
    file_name = 'write.mp4'
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    download_begin = datetime.datetime.now()
    s3.download_file(bucket_name, file_name, "write.mp4")
    download_size = os.path.getsize("write.mp4")
    download_stop = datetime.datetime.now()
    
    process_begin = datetime.datetime.now()
    upload_path = video_to_gif_ffmpeg("write.mp4", duration, event)
    process_end = datetime.datetime.now()
    
    upload_begin = datetime.datetime.now()
    upload_size = os.path.getsize(upload_path)
    s3.upload_file('write.gif', bucket_name, 'write.gif')
    upload_stop = datetime.datetime.now()
    
    download_time = (download_stop - download_begin) / datetime.timedelta(microseconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)
    upload_time = (upload_stop - upload_begin) / datetime.timedelta(microseconds=1)
    
    return { 'result': {'bucket': bucket_name, 'file name': "write.gif"} , 
    	     'measurement': {'download time': download_time, 'size' : download_size, 'upload size': upload_size, 'compute time': process_time, 'upload_time': upload_time} }


def main(params):
    resultat = handler({})
    return  resultat
