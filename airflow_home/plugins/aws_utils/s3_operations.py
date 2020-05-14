import configparser
import boto3


def upload_code():
    # Config parser
    config = configparser.ConfigParser()
    config.read('airflow_home/dl.cfg')
    etl_file = config['SPARK']['FILE_PATH']

    s3_client = boto3.client(
        's3',
        region_name='us-west-2',
        aws_access_key_id=config['AWS']['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=config['AWS']['AWS_SECRET_ACCESS_KEY'],
    )
    etl_bucket = config['S3']['CODE_BUCKET']
    s3_client.upload_file(etl_file, etl_bucket, 'etl.py')


def create_s3_buckets():
    # Config parser
    config = configparser.ConfigParser()
    config.read('airflow_home/dl.cfg')
    # S3 settings
    s3_client = boto3.client(
        's3',
        region_name='us-west-2',
        aws_access_key_id=config['AWS']['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=config['AWS']['AWS_SECRET_ACCESS_KEY'],
    )
    s3_resource = boto3.resource('s3')

    etl_bucket = config['S3']['CODE_BUCKET']
    etl_output_bucket = config['S3']['OUTPUT_BUCKET']
    emr_log_bucket = config['S3']['LOG_BUCKET']

    create_bucket(s3_client, s3_resource, etl_output_bucket)
    create_bucket(s3_client, s3_resource, etl_bucket)
    create_bucket(s3_client, s3_resource, emr_log_bucket)


def create_bucket(s3_client, s3_resource, bucket_name):
    location = {'LocationConstraint': 'us-west-2'}
    if not s3_resource.Bucket(bucket_name).creation_date:
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

#
