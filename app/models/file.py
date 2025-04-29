from requests import Session
from app import db
from datetime import datetime
import pytz 
from sqlalchemy import and_

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    firebase_uid = db.Column(db.String(128), nullable=False)  
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50),nullable=True)  
    file_size = db.Column(db.Integer,nullable=True)
    path = db.Column(db.String(1024), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    accessed_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    __table_args__ = (db.UniqueConstraint('firebase_uid', 'file_name', 'path', name='unique_file_per_user_folder'),)

    def __repr__(self):
        return f"<File {self.file_name} ({self.file_type}) in {self.firebase_uid}>"

    
    @classmethod
    def create(cls, firebase_uid: str, file_name: str, file_type: str, file_size: int, path=None):
        print(f"Entered create function with: {firebase_uid=}, {file_name=}, {file_type=}, {file_size=}, {path=}")
        try:
            if not firebase_uid or not file_name or not file_size:
                print("Validation failed: Missing required fields")
                return None

            new_file = cls(
                firebase_uid=firebase_uid,
                file_name=file_name,
                file_type=file_type,
                file_size=file_size,
                path=path
            )
            db.session.add(new_file)
            db.session.commit()
            print(f"File successfully created: {new_file}")
            return new_file

        except Exception as e:
            import traceback
            db.session.rollback()
            print(f"Error creating file: {e}")
            print(traceback.format_exc())
            return None

    
    def mark_accessed(self):
        self.accessed_at = datetime.utcnow()
        db.session.commit()

    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting file: {e}")
            
    @classmethod
    def fetch_recently_accessed_files(cls, firebase_id: str, limit: int = 10):
        try:
            from app.models.file import File
            if not firebase_id:
                print("Firebase id is not received")
                return None
            files = cls.query.filter_by(firebase_uid=firebase_id).order_by(File.accessed_at.desc()).limit(limit).all()
            return files
        except Exception as e:
            print(f"Error fetching recently accessed files: {e}")
            return None
            
    @classmethod
    def fetch_files_in_folder(cls, folder_path, firebase_id):
        try:
            print("Fodler path : ",folder_path)
            print()
            files = cls.query.filter(
            and_(
                cls.firebase_uid == firebase_id,
                cls.path.like(f"{folder_path + '/'}%")
            )
        ).all()
            
            if not files:
                return None
            else:
                return files
        except Exception as e:
            print(f"Error fetching files in folder : {e}")
            return None
            
            
            
            
               
        
        
        
        
        
    
    