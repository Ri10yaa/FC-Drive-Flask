from requests import Session
from app import db
from datetime import datetime
from sqlalchemy import Column,DateTime, and_
import pytz

class Folder(db.Model):
    __tablename__ = 'folders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firebase_uid = db.Column(db.String(128), nullable=False)
    folder_name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(1024), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    __table_args__ = (
        db.UniqueConstraint('firebase_uid', 'folder_name', 'path', name='unique_folder_per_user_path'),
    )

    def __repr__(self):
        return f"<Folder {self.folder_name} for {self.firebase_uid}>"

    @classmethod
    def create(cls, firebase_uid, folder_name, path=None):
        try:
            if not firebase_uid or not folder_name:
                print("Firebase id or folder is not received")
                return None
            
            new_folder = cls(
                firebase_uid=firebase_uid,
                folder_name=folder_name,
                path=path
            )
            db.session.add(new_folder)
            db.session.commit()
            return new_folder
        except Exception as e:
            db.session.rollback()
            print(f"Error creating folder: {e}")
            return None
        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting folder: {e}")
            
    @classmethod
    def fetch_all_folders(cls,firebase_id):
        try:
            if not firebase_id:
                print("Invalid firebase ID\n")
                return None
            folders = cls.query.filter_by(firebase_uid=firebase_id,path=None)
            
            if not folders:
                return None
            else:
                return folders
        except Exception as e:
            print(f"Error while fetching all folders : {e}")
            return None
            
    @classmethod
    def fetch_folders_in_folder(cls, folder_path, firebase_id):
        print("Entered fetch fodler folder path : ", folder_path + "/")
        try:
            folders = cls.query.filter(
            and_(
                cls.firebase_uid == firebase_id,
                cls.path.like(f"{folder_path}%")
            )
        ).all()
            print(folders)
            if not folders:
                return None
            else:
                
                return folders
        except Exception as e:
            print(f"Error fetching folders in folder : {e}")
            return None
             
            
    '''
    @classmethod
    def list_user_folders(cls, firebase_uid):
        return cls.query.filter_by(firebase_uid=firebase_uid).all()
    
    @classmethod
    def get_folder_by_name_and_parent_folder(cls, firebase_id,folder_name, parent_folder_name):
        return cls.query.filter_by(firebase_id=firebase_id, folder_name=folder_name, pa)
    
    # @classmethod
    # def get_folder_id(cls, firebase_uid, folder_name, parent_folder_id=None):
    #     """
    #     Get the folder ID when firebase_uid and folder_name are given.
    #     Optionally, filter by parent_folder_id for nested folders.
    #     """
    #     try:
    #         folder_name = folder_name.strip('/')
            
    #         query = cls.query.filter_by(firebase_uid=firebase_uid, folder_name=folder_name)
            
    #         if parent_folder_id is not None:
    #             query = query.filter_by(parent_folder_id=parent_folder_id)
            
    #         folder = query.first()

    #         if not folder:
    #             raise ValueError("Folder not found")
            
    #         return folder.id
    #     except Exception as e:
    #         print(f"Error fetching folder ID: {e}")
    #         return None
        
    @classmethod
    def get_folder_details(cls, firebase_uid, folder_name):
        """
        Fetch the folder details (folder ID and parent folder ID) based on firebase_uid and folder_name.
        """
        try:
            # Normalize the folder name
            folder_name = folder_name.strip('/')

            # Query the folder details
            folder = cls.query.filter_by(firebase_uid=firebase_uid, folder_name=folder_name).first()
            if not folder:
                raise ValueError("Folder not found")

            return {"folder_id": folder.id, "parent_folder_id": folder.parent_folder_id}
        except Exception as e:
            print(f"Error fetching folder details: {e}")
            return None


    
    '''       
    
