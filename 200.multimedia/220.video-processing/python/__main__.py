import numpy
import datetime
import os
import subprocess
import boto3
from os import path



def call_ffmpeg(args):
    ret = subprocess.run(["ffmpeg", '-y'] + args,
            #subprocess might inherit Lambda's input for some reason
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if ret.returncode != 0:
        print('Invocation of ffmpeg failed!')
        print('Out: ', ret.stdout.decode('utf-8'))
        raise RuntimeError()



# https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality
def to_gif(video, duration, event):
    output = 'write.gif' 
    call_ffmpeg(["-i", video,
        "-t",
        "{0}".format(duration),
        "-vf",
        "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "-loop", "0",
        output])
    return output


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
    upload_path = to_gif("write.mp4", duration, event)
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
