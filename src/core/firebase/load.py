import os
import firebase_admin
from firebase_admin import credentials

current_directory = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_directory, 'credentials.json')

cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred,{'storageBucket': 'new-york-42e41.appspot.com'})