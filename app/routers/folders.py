from flask import Flask, request, jsonify, Blueprint, session
from flask_cors import CORS
from app import db

folders_bp = Blueprint('folders', __name__)
CORS(folders_bp, supports_credentials=True)

# create folder
@folders_bp.route('/create', methods=['POST'])
def create_folder():
    try:
        from app.models.folder import Folder
        data = request.get_json()
        firebase_id = data.get('firebase_id')
        folder_hiearchy = data.get('folder_hiearchy')
        folder_name = data.get('folder_name')
        
        if folder_hiearchy:
            folder_path = ('/').join(folder_hiearchy)
        else:
            folder_path= None
            
        print(firebase_id)
        print(folder_hiearchy)
        print(folder_name)    
        
            
        new_folder = Folder.create(
            firebase_uid=firebase_id,
            folder_name=folder_name,
            path=folder_path
        )
        
        if new_folder:
            
            return jsonify({"msg" : "Folder created successfully", "folder_id" : new_folder.id}), 200
        else:
            return jsonify({"msg" : "Folder not created."}),500
    except Exception as e:
        return jsonify({"msg" : "Error while creating folder","error" : "${e}"}), 500
        


# Fetch folder contents
# Needs folder hiearchy in request body
@folders_bp.route('/<string:firebase_id>/<string:pathString>',methods=['GET'])
def fetch_folder_contents(folder_name, firebase_id, pathString):
    try:
        files, folders = [], []
        print("The path string is : ",pathString,"\n")
        from app.models.file import File
        from app.models.folder import Folder
        
        if pathString is None:
           folders = Folder.fetch_all_folders(firebase_id=firebase_id) 
        else:
            files = File.fetch_files_in_folder(pathString,firebase_id)
            folders = Folder.fetch_folders_in_folder(pathString,firebase_id)
            
        
        if not files or folders:
            return jsonify({"msg" : "No contents"}), 200  
        
        if folders is not None:
             serialized_folders = [
            {
                "id" : folder.id,
                "folder_name" : folder.folder_name,
                "path" : folder.path,
                "created_at" :  folder.created_at.isoformat() if folder.created_at else None
            }
            for folder in folders
        ]
        
        if files is not None:
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
       
        return jsonify({"msg" : "Retrieved folder contents", "files" : serialized_files, "folders" : serialized_folders}), 200
    except Exception as e:
        return jsonify({"msg" : "Failed retrieving folder contents", "error" : "${e}"}),500
    
        
# @folders_bp.route('/<string:firebase_id>/all',methods=['GET'])    
# def fetch_all_folders(firebase_id):
#     try:
#         from app.models.folder import Folder
#         folders = Folder.fetch_all_folders(firebase_id=firebase_id)

#         if not folders:
#             return jsonify({"msg" :"No folders found"}), 200
#         else:
#             serialized_folders = [
#                 {
#                     "id" : folder.id,
#                     "folder_name" : folder.folder_name,
#                     "path" : folder.path,
#                     "created_at" :  folder.created_at.isoformat() if folder.created_at else None
#                 }
#                 for folder in folders
#             ]
#             return jsonify({"msg" : "Folders retreived", "folders" : serialized_folders}), 200
#     except Exception as e:
#         print("Entered exception\n")
#         return jsonify({"msg" :"Failed to retrieve all folders","error" : str(e)}), 500
    
    
        




























'''
#fetch all folders
@folders_bp.route('/<string:user_id>', methos=['GET'])
def fetch_folders_by_user(user_id):
    try:
        from app.models import folder  

        folders = folder.list_user_folders(user_id)

        if not folders:
            return jsonify({"msg": "No folders found"}), 404
        
        folder_data = [
            {
                "id": folder.id,
                "firebase_uid": folder.firebase_uid,
                "folder_name": folder.folder_name,
                "created_at": folder.created_at,
            }
            for folder in folders
        ]

        return jsonify({"folders": folder_data}), 200
    except Exception as e:
        print(f"Error fetching folders: {e}")
        return jsonify({"msg": "Error fetching folders", "error": str(e)}), 500
'''