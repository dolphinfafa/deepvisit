import os
from datetime import timedelta

class Config:
    """应用配置类"""
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-deepvisit-2024'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///deepvisit.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # 上传文件配置
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'xls', 'csv'}

