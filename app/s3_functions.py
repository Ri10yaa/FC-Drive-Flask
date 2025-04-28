import boto3
from flask import jsonify
import os
from app.models import folder
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

    

        
    
 