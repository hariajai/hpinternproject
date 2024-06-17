import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', "b'\xa7P\xc59k\xc6\x84:\x03\x82\x03\xa6\x0b\xefl\r\xb9\x8b\xbe\xec\x89pz\x86'")
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'hphar')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'hari')
    MYSQL_DB = os.getenv('MYSQL_DB', 'flask_app')


   
    
