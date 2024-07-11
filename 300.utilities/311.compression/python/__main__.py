import datetime
import io
import os
import uuid
import zlib
import boto3
import zipfile




def handler(event):
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
    output_zip = 'write.zip'
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        zipf.write("write.mp4", arcname="write.mp4")	
    process_end = datetime.datetime.now()
    
    upload_begin = datetime.datetime.now()
    s3.upload_file('write.zip', bucket_name, 'write.zip')
    upload_stop = datetime.datetime.now()
    upload_size = os.path.getsize("write.zip")
    
    download_time = (download_stop - download_begin) / datetime.timedelta(microseconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)
    upload_time = (upload_stop - upload_begin) / datetime.timedelta(microseconds=1)
    
    return { 'result': {'bucket': bucket_name, 'file name': "write.zip"} , 
    	     'measurement': {'download time': download_time, 'size' : download_size, 'upload size': upload_size, 'compute time': process_time, 'upload_time': upload_time} } 


def main(params):
    resultat = handler({})
    return  resultat
    

#if __name__ == "__main__":
    #main({})
