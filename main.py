from flask import Flask, render_template, request, url_for, redirect, flash
from pymongo import MongoClient
from crop_stuff import grab
import os
from bson import ObjectId
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime

from forms import *

mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_host = os.getenv("MONGO_HOST")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")

atlas = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_host}"
print("atlas: ", atlas)
client = MongoClient(atlas)
db = client.test_database
products = db.products
users = db.users
images = db.images
inventory = db.inventory
groups = db.groups
colors = db.colors
user_info = db.user_info

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = flask_secret_key
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User:
    def __init__(self, b_email, user_type, the_id, role, username, pic):
        self.email = b_email
        self.user_type = user_type
        self.id = the_id
        self.role = role
        self.username = username
        self.pic = pic
    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def data(self):
        pack = {
            "email": self.email,
            "username": self.username,
            "role": self.role,

        }
        return pack

    @staticmethod
    def is_admin(self):
        if self.user_type == 'admin':
            return True
        else:
            return False

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def check_password(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)


    @login_manager.user_loader
    def load_user(id):
        u = users.find_one({"_id": ObjectId(id)})
        if not u:
            return None #or false
        return User(b_email=u['email'], user_type=u['type'], the_id=u['_id'], role=u['role'], username=u['username'], pic=u['pic'])
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

@app.route("/", methods=['GET'])
def index():
    if request.method == "GET":
        b_list = ["lime.png", "blueberry.png", "bluestripe.png", "majestic.png", "pom.png", "vortex.png"]
        inv = inventory.find({"status":1})
        return render_template("build_shop.html", p_list=inv, b_list=b_list, title="Home")
    elif request.method == "POST":
        return True

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.find_one({"email": form.email.data})
        if user and User.check_password(user['password'], form.password.data):
            user_obj = User(b_email=user['email'], user_type=user['type'], the_id=str(user['_id']), role=user['role'], username=user['username'], pic=user['pic'])
            login_user(user_obj, remember=form.remember.data)
            if user['type'] == 'admin':
                next_page = url_for('admin_dashboard')
            else:
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash("Invalid username or password")
            print("else state hit!!!!!!!!!!")

    else:
        print("form not validated")
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['GET'])
def logout():

        logout_user()
        #flash('you are now logged out.')
        #user haas to be logged in to log out
        return redirect(url_for('index'))



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        c_check = users.find_one({"email": form.email.data})
        print("c_check: ", c_check)
        if c_check:
            flash("Email already exists! sign in<a href='/login'>here</a>....<a/forgot_password>Forgot password?</a>",
                  "error")
            return render_template('signup.html', form=form)
        else:
            flash(f'Account created for {form.username.data}! You are now able to login.', 'success')
            print("form valid, check valid")
            password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            pack = {
                "email": form.email.data,
                "username": form.username.data,
                "password": password,
                "type": "user",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.now(),
                "status": "unverified",
                "role": "Customer",
                "pic": ""
            }
            users.insert_one(pack)
            print("done.")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    update_email_form = UpdateEmail_ProfileForm()
    update_password_form = UpdatePassword_ProfileForm()
    update_stat_form = UpdateStatForm()
    if current_user.is_authenticated and request.method == "GET":
        print("blocked")
        return render_template('profile.html', user=current_user, update_email_form=update_email_form, update_password_form=update_password_form, update_stat_form=update_stat_form, title="Your Profile")
    if update_email_form.validate_on_submit():
        print("update email")
        new_email = update_email_form.new_email.data
        check_email = users.find_one({"email": new_email})
        if check_email:
            print("check_email")
            pass
        else:
            print("new_email: ", new_email)
            email_query = users.find_one({"email": current_user.get_id()})
            if email_query:
                the_email = email_query['email']
                # send verification email- make route to recieve verification
                # add it to email change list
                users.update_one({"_id": ObjectId(email_query['_id'])}, {"$set": {"email": new_email}})
            else:
                flash("Email doesn't exist")
        return redirect(url_for('profile'))
    elif update_password_form.validate_on_submit():
        print("update password")
        current_password = update_password_form.old_password.data
        use = users.find_one({"_id": ObjectId(current_user.get_id())})  #should be _id
        if use:
            p_word_check = User.check_password(use['password'], current_password)
            if p_word_check:
                print("p_word_check")
                #add flashing
                new_password = update_password_form.new_password.data
                p_word = bcrypt.generate_password_hash(new_password).decode('utf8')
                users.update_one({"_id": ObjectId(current_user.get_id())}, {"$set": {"password": p_word}})
                return redirect(url_for('profile'))
            else:
                print("Incorrect password")
                flash("Incorrect password. Try again!", "error")
                return redirect(url_for('profile'))
        else:
            print("big error")
    elif update_stat_form.validate_on_submit():
        print("update stat")
        f_name = update_stat_form.first_name.data
        l_name = update_stat_form.last_name.data
        address = update_stat_form.address.data
        state = update_stat_form.state.data
        city = update_stat_form.city.data
        zip = update_stat_form.zip.data
        unit = update_stat_form.unit.data
        phone = update_stat_form.phone.data

        pack = {
            "first_name": f_name,
            "last_name": l_name,
            "address": address,
            "state": state,
            "city": city,
            "zip": zip,
            "unit": unit,
            "phone": phone,
            "timestamp": datetime.utcnow(),
            "user_ref": current_user.get_id(),
        }
        user_info.insert_one(pack)
        return redirect(url_for('profile'))
    else:
        print("big error")
        flash("error", "error")
        return redirect(url_for('profile'))


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


@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if current_user.is_authenticated and current_user.is_admin:
        the_inv = inventory.find({"status": 1})
        the_admins = []
        usersi = users.find({"type": "admin"})
        for user in usersi:
            if user['username'] != current_user.username:
                the_admins.append(user['pic'])
        return render_template("admin_dashboard.html", inventory=the_inv, the_admins=the_admins)

@app.route("/promo", methods=["GET", "POST"])
def promo():
    if request.method == "GET":
        return "<br><a href='/'>Go Back</>"


"""if __name__ == '__main__':
    app.run(debug=True)"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)