from flask import Flask, request, jsonify, Blueprint, session
from firebase_admin import credentials, auth
from flask_cors import CORS
import firebase_admin
import os
from app.encryption_decryption import encrypt, decrypt 
from firebase_admin import auth


cred = credentials.Certificate(
    "/home/rithanyaa/Documents/cloudpro/FC_drive/backend/firebase/fcstorage-c0cf0-firebase-adminsdk-fbsvc-6fd74faf5f.json"
)
firebase_admin.initialize_app(cred)


auth_bp = Blueprint('auth', __name__)
CORS(auth_bp, supports_credentials=True)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        from urllib.parse import unquote

        password = unquote(data.get('password'))

        if not email or not password:
            return jsonify({"msg": "Email and password are required"}), 400

        from app.models.user import User

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "User not found!"}), 404

        if user.password != password:
            return jsonify({"msg": "Invalid password!"}), 401

        firebase_user = auth.get_user_by_email(email)
        firebase_uid = firebase_user.uid
        encrypted_uid = encrypt(firebase_uid)

        return jsonify({
            "msg": "Login successful",
            "id": user.id,
            "email": user.email,
            "password": encrypt(user.password),
            "fuid": encrypted_uid,
        }), 200

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"msg": "Error during login", "error": str(e)}), 500




@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        from app.models.user import User
        
        try:
            firebase_user = auth.get_user_by_email(email)
            return jsonify({"error": "Firebase user already exists", "firebase_uid": firebase_user.uid}), 400
        except:
            pass

        firebase_user = auth.create_user(
            email=email,
            password=password
        )
        firebase_uid = firebase_user.uid
        print("Firebase UID:", firebase_uid)

        encrypted_uid = encrypt(firebase_uid)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        new_user = User.create(
            email=email,
            password=password,
            firebase_uid=firebase_uid  
        )

        return jsonify({
            "msg": "Signup successful",
            "firebase_uid": encrypted_uid,  
            "id": new_user.id,
            "email": new_user.email,
            "password": encrypt(new_user.password),  
        }), 200

    except Exception as e:
        print(f"Error during signup: {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
def profile():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized. Please login first"}), 401

    return jsonify({"message": "Profile retrieved successfully", "user": session['user']}), 200


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200
