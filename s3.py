import boto3
import os
from botocore.exceptions import ClientError
from configparser import ConfigParser

cwd = os.getcwd()
file = cwd+'/config.ini'
config = ConfigParser()
config.read(file)


class S3:
    bucket_name = config['aws']['bucket_name']
    wrk_dir = 'sdk/aws/'

    def __init__():
        print('constructor intantiated...')

    def download_file(file_name):
        client_s3 = boto3.client(
            config['aws']['service_type'],
            region_name=config['aws']['region_name'],
            aws_access_key_id=config['aws']['access_key_id'],
            aws_secret_access_key=config['aws']['secret_access_key']
        )
        try:
            client_s3.download_file(S3.bucket_name, file_name, os.path.join(os.getcwd(), 'Process/' + file_name))
            return True
        except Exception as e:
            return e

    def list_files():
        client_s3 = boto3.resource(
            config['aws']['service_type'],
            region_name=config['aws']['region_name'],
            aws_access_key_id=config['aws']['access_key_id'],
            aws_secret_access_key=config['aws']['secret_access_key']
        )
        my_bucket = client_s3.Bucket(S3.bucket_name)
        file_names = []
        for my_bucket_object in my_bucket.objects.all():
            file_names.append(my_bucket_object.key)

        return file_names

    def upload_files():
        client_s3 = boto3.client(
            config['aws']['service_type'],
            region_name=config['aws']['region_name'],
            aws_access_key_id=config['aws']['access_key_id'],
            aws_secret_access_key=config['aws']['secret_access_key']
        )
        data_file_folder = os.path.join(os.getcwd(), S3.wrk_dir + 'Uploads')

        for file in os.listdir(data_file_folder):
            if not file.startswith('~'):
                try:
                    print('Uploading File {0}...'.format(file))
                    client_s3.upload_file(
                        os.path.join(data_file_folder, file),
                        S3.bucket_name,
                        file
                    )
                except ClientError as e:
                    print('Credentials are incorrect')
                    print(e)
                except Exception as e:
                    print(e)
