from pymongo import MongoClient
import glob
from datetime import datetime
from PIL import Image
client = MongoClient('localhost', 27017)
db = client.test_database
imms = db.images
hailey_files = glob.glob("static/assets/mockups/*")
print(hailey_files)
"""for h_file in hailey_files:

    pack = {
        "timestamp": datetime.now(),
        "filename": h_file,
        "status": 0
    }
    imms.insert_one(pack)"""
count = 1
for h_file in hailey_files:
    print(f"{h_file} - count: ", count)
    count += 1
    img = Image.open(h_file)
    resized = img.resize((480,480), Image.LANCZOS)
    resized.save(h_file)