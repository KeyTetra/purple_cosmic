from click.decorators import pass_meta_key
from pymongo import MongoClient
import glob
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.test_database
users = db.users


pack_holder = []
hailey_pack = {
"email": "thepurplecosmic@gmail.com",
"username": "Hey_Hey",
"password": "",
"type": "admin",
"created_at": datetime.utcnow(),
"updated_at": datetime.now(),
"status": "unverified",
"role": "CEO"
}
pack_holder.append(hailey_pack)
key_pack = {
    "email": "keymtetra@gmail.com",
    "username": "Key",
    "password": "",
    "type": "admin",
    "created_at": datetime.utcnow(),
    "updated_at": datetime.now(),
    "status": "unverified",
    "role": "CTO"
}
pack_holder.append(key_pack)

for p in pack_holder:
    password = input("Enter password: ")
