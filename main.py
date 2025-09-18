from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from crop_stuff import grab
import os
from bson import ObjectId
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import datetime

mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_host = os.getenv("MONGO_HOST")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")

atlas = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_host}"
client = MongoClient(atlas)
db = client.test_database
products = db.products
users = db.users
images = db.images
inventory = db.inventory
groups = db.groups
colors = db.colors

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = flask_secret_key
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User:
    def __init__(self, b_email):
        self.business_email = b_email

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.business_email

    @staticmethod
    def check_password(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)


    @login_manager.user_loader
    def load_user(b_email):
        u = users.find_one({"business_email": b_email})
        if not u:
            return None #or false
        return User(b_email=u['business_email'])
# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''

@app.route("/")
def index():
    if request.method == "GET":
        b_list = ["lime.png", "blueberry.png", "bluestripe.png", "majestic.png", "pom.png", "vortex.png"]
        inv = inventory.find({"status":1})
        return render_template("build_shop.html", p_list=inv, b_list=b_list)
    elif request.method == "POST":
        return True

@app.route("/login")
def hello_world():
    if request.method == "GET":
        p_list = ["bahlsen-g.webp", "Hanuta-600-g.webp", "ktkt.avif", "mentai.webp", "seafood.webp"]
        return render_template("login.html")
    elif request.method == "POST":
        return True



@app.route("/bulk_shop")
def bulk_shop():
    if request.method == "GET":
        p_list = ["bahlsen-g.webp", "Hanuta-600-g.webp", "ktkt.avif", "mentai.webp", "seafood.webp"]
        return render_template("layout.html", p_list=p_list)
    elif request.method == "POST":
        return True

@app.route("/shopping_cart")
def shopping_cart():
    if request.method == "GET":
        p_list = ["bahlsen-g.webp", "Hanuta-600-g.webp", "ktkt.avif", "mentai.webp", "seafood.webp"]
        return render_template("layout.html", p_list=p_list)
    elif request.method == "POST":
        return True


@app.route("/crop", methods=["GET", "POST"])
def crop():
    if request.method == "GET":
        imm = images.find_one({"status": 0})
        print("imm: ",imm)
        return render_template("crop.html", image=imm['filename'])
    elif request.method == "POST":
        the_x = request.form['x']
        the_y = request.form['y']
        the_w = request.form['width']
        the_h = request.form['height']
        print("stuff:", the_x, the_y, the_w, the_h)
        the_image = request.form['image']
        i_file = os.path.join(the_image)
        gf = grab(i_file, (int(float(the_x)), int(float(the_y)), int(float(the_w)), int(float(the_h))))
        t_i = images.find_one({"status": 0, "filename": i_file})
        if t_i:
            images.update_one({"_id": ObjectId(t_i['_id'])}, {"$set": {"status": 1, "cropped_filename": gf["out"]}})
        else:
            print("didnt hit")
        return render_template("crop2.html", image=gf["out"])
    else:
        return None


@app.route("/crop2", methods=["POST"])
def crop2():
    if request.method == "POST":
        the_image = request.form['image']
        crop_con = request.form['crop_con']
        if crop_con == "good":
            images.update_one({"cropped_filename": the_image}, {"$set": {"status": 2}})
        else:
            images.update_one({"cropped_filename": the_image}, {"$set": {"status": 0}})
        return redirect(url_for("crop"))


@app.route("/inventory_maker", methods=["GET", "POST"])
def inventory_maker():
    if request.method == "GET":
        ccolors = colors.find()
        the_colors = [c['name'] for c in ccolors]
        ggroups = groups.find()
        the_groups = [g['name'] for g in ggroups]
        print("ccolors: ", the_colors)
        print("ggroups: ", the_groups)
        for group in the_groups:

            for color in the_colors:
                on_off = False

                print("group: ", group, " color: ", color)
                productss = products.find({"color": color, "group": group})
                p_count = 0
                prod_keeper = []
                imm_keeper = []
                for prod in productss:
                    if prod['status'] == 0:
                            prod_keeper.append(prod['_id'])
                            print("prod: ", prod)
                            imm = images.find_one({"_id": ObjectId(prod['product_id'])})
                            print("imm: ", imm)
                            if imm:
                                print("imm: ", imm)
                                imm_keeper.append({"image_id": imm['_id'], "cropped_im": imm["cropped_filename"]})
                            else:

                                print("no match")
                                pass
                    else:
                        pass
                if len(imm_keeper) > 0:
                    pack = {
                                        "group": group,
                                        "color": color,
                                        "products": imm_keeper,
                                        "price": "",
                                        "timestamp": datetime.datetime.utcnow(),
                                        "status": 0
                    }


                    print("PACK: ", pack)
                    inventory.insert_one(pack)
                    for prodi in prod_keeper:
                        print("prod: ", prodi)
                        products.update_one({"_id": ObjectId(prodi)}, {"$set": {"status": 1}})
                else:
                    pass

        inve = inventory.find({"status": 0})
        print("inv: ", inve)
        return render_template("inventory_maker.html", pproducts=inve)
    elif request.method == "POST":
        price = request.form['price']
        title = request.form['title']
        product_id = request.form['product_id']
        inventory.update_one({"_id": ObjectId(product_id)}, {"$set": {"price": price, "status": 1, "title": title}})
        return redirect(url_for("inventory_maker"))
"""
@app.route("/inventory_maker2", methods=["GET", "POST"])
def inventory_maker2():
    if request.method == "GET":
        ccolors = colors.find()
        ggroups = groups.find()
        the_list = []
        for group in ggroups:
            for color in ccolors:
                iin = inventory.find_one({"color": color["name"], "group": group["name"]})
                if iin:
                    pass
                else:
                    productss = products.find({"color": color["name"], "group": group["name"]})
                    if productss:
                        product_ids = [pr["product_id"] for pr in productss]
                        imm_keeper = []
                        for p in product_ids:
                            imm = images.find_one({"_id": ObjectId(p)})
                            if imm:
                                imm_keeper.append({"image_id": imm['_id'], "cropped_im": imm["cropped_filename"]})
                        pack = {
                            "group": group['name'],
                            "color": color['name'],
                            "products": imm_keeper,
                            "price": "",
                            "timestamp": datetime.datetime.utcnow(),
                        }
                        new = inventory.insert_one(pack)
                        print("new: ", new)
                        the_list.append({"pack": pack, "_id": new.inserted_id})
                    else:
                        pass"""
@app.route("/add_color", methods=["GET", "POST"])
def add_color():
    if request.method == "GET":
        col = colors.find()
        return render_template("add_color.html", colors=col)
    if request.method == "POST":
        col = request.form['color']
        c = colors.find_one({"name": col})
        if c:
            pass
        else:
            colors.insert_one({"name": col})
        return redirect(url_for("add_color"))


@app.route("/add_group", methods=["GET", "POST"])
def add_group():
    if request.method == "GET":
        col = groups.find()
        return render_template("add_group.html", groups=col)
    if request.method == "POST":
        col = request.form['group']
        c = groups.find_one({"name": col})
        if c:
            pass
        else:
            groups.insert_one({"name": col})
        return redirect(url_for("add_group"))

@app.route("/product_maker", methods=["GET", "POST"])
def product_maker():
    if request.method == "GET":
        pproducts = images.find({"status": 2})
        ccolors = colors.find()
        ggroups = groups.find()
        return render_template("product_maker.html", pproducts=pproducts, groups=ggroups, colors=ccolors)
    if request.method == "POST":
        ccolor = request.form['color']
        gg = request.form['group']
        pp = request.form['product_id']
        products.insert_one({"group": gg, "product_id": pp, "color": ccolor, "status": 0})
        images.update_one({"_id": ObjectId(pp)}, {"$set": {"status": 3}})
        return redirect(url_for("product_maker"))

if __name__ == '__main__':
    app.run(debug=True)