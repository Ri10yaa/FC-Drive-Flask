from app import db
from datetime import datetime
import pytz

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(0), nullable=False)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    
    @classmethod
    def create(cls, email, firebase_uid, password):
        user = cls(email=email, firebase_uid=firebase_uid, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def to_dict(self):
        return {
            "email": self.email,
            "password" : self.password
        }

    @classmethod
    def get_by_id(cls,user_id):
        return cls.query.get(user_id)
    
    @classmethod
    def get_by_firebase_uid(cls, firebase_uid):
        return cls.query.filter_by(firebase_uid=firebase_uid).first()
    
    def update_email(self, new_email):
        self.email = new_email
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
