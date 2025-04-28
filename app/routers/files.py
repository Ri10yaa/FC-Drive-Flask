from flask import Flask, request, jsonify, Blueprint, session
from flask_cors import CORS
from app import db
import os
import json
from app.s3_functions import upload_to_s3
from app import db
from app.encryption_decryption import decrypt

files_bp = Blueprint('files', __name__)
CORS(files_bp, supports_credentials=True)

def create_file_path(filename, folder_hiearchy):
    if folder_hiearchy:
        file_path = "/".join(folder_hiearchy)
    else:
        file_path = f"/{filename}"
    return file_path

# upload file
@files_bp.route('/upload', methods = ['POST'])
def upload_file():
    try:
        file = request.files.get('file')  
        json_data = request.form.get('metadata')
        
        if not file or not json_data:
            return jsonify({'error': 'Missing file or metadata'}), 400
        
        data = json.loads(json_data)
        firebase_id = data.get('firebase_id')
        filename = data.get('file_name')
        folder_hiearchy = data.get('folder_hiearchy')
        file_size = data.get('file_size')
        file_type = data.get('file_type')
    
        
        file_path = create_file_path(filename,folder_hiearchy)
        
        s3_key = firebase_id + file_path
        
        isUploaded = upload_to_s3(file,s3_key)
        print("Uploaded : ",isUploaded)
        
        if isUploaded:
            from app.models.file import File
            print(firebase_id)
            print(filename)
            print(file_type)
            print(file_path)
            print(file_size)
            
            new_file = File.create(
                firebase_uid=firebase_id,
                file_name=filename,
                file_type=file_type,
                file_size=file_size,
                path=file_path
            )
            
            if new_file:
                return jsonify({"msg" : "Uploaded successfully","file_id" : new_file.id}), 200
            else:
                return jsonify({"msg" : "Error ocured in storing in DB."}), 500
            
        else:
            return jsonify({"msg" : "File not uploaded in S3"}),500
    except Exception as e:
        return jsonify({"msg" : "Error occured during upload ", "error" : "${e}"}),500

# fetch recent files
@files_bp.route('/recent/<string:user_id>',methods=['GET'])
def fetch_recent_files(user_id):
    try:
        from app.models.file import File
        files = File.fetch_recently_accessed_files(user_id)
        
        if files:
            serialized_files = [
                {
                    "file_name": file.file_name,
                    "file_type": file.file_type,
                    "file_size": file.file_size,
                    "path": file.path,
                    "accessed_at": file.accessed_at.isoformat() if file.accessed_at else None
                }
                for file in files
            ]
            print(serialized_files)
            return jsonify({"msg": "Files retrieved", "files": serialized_files}), 200
        else:
            return jsonify({"msg": "No files retrieved"}), 404
    except Exception as e:
        print(f"Error while fetching files: {e}")
        return jsonify({"msg": "Error while fetching files", "error": str(e)}), 500

   















