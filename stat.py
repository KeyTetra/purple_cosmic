import os
from pymongo import MongoClient
from bson import ObjectId



atlas = "mongodb+srv://keytetra:WfcIa60ygAEYFu3a@cluster0.ob4vmq9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(atlas)
db = client.test_database
inventory = db.inventory


for product in inventory.find():
    prod_list = []
    the_list = product['products']
    for prd in the_list:
        the_id = prd['image_id']
        the_real_string = prd['cropped_im']
        path_parts = os.path.join(*the_real_string.split(os.sep)[1:])
        print(path_parts)
        pack = {
            "image_id": the_id,
            "cropped_image": path_parts,

        }
        prod_list.append(pack)
    inventory.update_one({"_id": ObjectId(product['_id'])}, {"$set":{"products": prod_list}})
