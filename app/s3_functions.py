import boto3
from flask import jsonify
import os
from app.models import folder
from io import BytesIO
from botocore.exceptions import NoCredentialsError, ClientError

s3 = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET')
        
def create_user_folder(firebase_uid, folder_name):
    try:
        s3_folder_key = f"{firebase_uid}/{folder_name.strip('/')}/"
        s3.put_object(Bucket=S3_BUCKET, Key=s3_folder_key)

        folder.create(firebase_uid, folder_name)

        return jsonify({'message': f'Folder created: {folder_name}'}), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
def upload_to_s3(file, s3_key):
    try:
        s3.upload_fileobj(
            file,  
            S3_BUCKET,  
            s3_key,  
            ExtraArgs={"ContentType": file.content_type}
        )
        return True
    except Exception as e:
        print(f"Error during file upload to S3: {e}")
        return False
    
def download_file_from_s3(file_key):
    try:
        file_stream = BytesIO()
        s3.download_fileobj(S3_BUCKET, file_key, file_stream)
        file_stream.seek(0)
        return file_stream
    
    except NoCredentialsError:
        raise Exception("AWS Credentials not available.")
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise Exception(f"File '{file_key}' does not exist in S3 bucket.")
        else:
            raise Exception(f"S3 Client Error: {e.response['Error']['Message']}")
    
    except Exception as e:
        raise Exception(f"Failed to download file from S3: {str(e)}")

    

        
    
 