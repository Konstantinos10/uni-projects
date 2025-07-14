import pyrebase
from private.firebase.firebase_config import firebaseConfig

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()