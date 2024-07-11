
import datetime
import os
import uuid
import boto3
import urllib.request
import urllib3
import requests
import wget


def upload(url):
    
    download_path = "video.mp4"
    # download_path = "photo.png"
    bucket_name = 'onanadbucket'
    file_name = 'write.mp4'
    # Storage connection
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    #Download the Files
    # process_begin = datetime.datetime.now()

    # ==============================================================
    # urllib.request.urlretrieve(url, filename=download_path)

    # ==============================================================
    # wget.download(url, download_path)

    # ==============================================================
    # http = urllib3.PoolManager()

    # ==============================================================
    # response = http.request('GET', url)
    # myfile = requests.get(url)
    # open(download_path, 'wb').write(response.data)

    # ===================================================
    chunk = 1024 * 6000
    r = requests.get(url, stream = True)
    with open("video.mp4", "wb") as vid:
        for chunk in r.iter_content(chunk_size = chunk):
            if chunk:
                vid.write(chunk)

    process_end = datetime.datetime.now()

    donwnload_size = os.path.getsize(download_path)


    #Upload the Files 
    # upload_begin = datetime.datetime.now()
    # s3.upload_file(download_path, bucket_name, 'photo.png')
    # upload_stop = datetime.datetime.now()
    # upload_size = os.path.getsize(download_path)

    download_time = (process_end - process_begin) / datetime.timedelta(seconds=1)
    # upload_time = (upload_stop - upload_begin) / datetime.timedelta(seconds=1)
    return {
             
            'measurement': {
                'download_time': download_time,
                'download_size': donwnload_size,
                # 'upload_time': upload_time,
                # 'upload_size': upload_size ,
                 
            }
    }



def main(args):
    result = upload("http://drive.google.com/uc?id=18mgSgoZabx5Yxr2lLfFGb59rqOSpH9Un&export=download")

    # return(result)
    print(result)






if __name__ == "__main__":
   main({})