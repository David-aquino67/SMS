import os


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/sms' 
SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_STORAGE = os.path.join(os.path.dirname(__file__), "storage")
API_TOKEN = "MI_TOKEN_SEGURO_12345"