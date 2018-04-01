
from flask import Flask, render_template, request, redirect,\
    jsonify, flash, url_for, abort, session as login_session
from sqlalchemy.orm.exc import NoResultFound
from hashlib import sha256
from os import urandom, remove
from uuid import uuid4

from utils.pixelate import PictureResizer
from utils.google_connect import GConnect
from utils.database_interact import DBInteractor
from utils.database_init import InventoryType, Category, Item, User, Skin

app = Flask(__name__)

# Database operation Helpers
inventoryDB = DBInteractor(InventoryType)
categoryDB = DBInteractor(Category)
userDB = DBInteractor(User)
itemDB = DBInteractor(Item)
skinDB = DBInteractor(Skin)

body_parts = ["head", "torso", "legs",
              "hands", "feet", "left_hand",
              "right_hand", "companion"]


def init():
    for part in body_parts:
        login_session[part] = {
            "image": "default.png",
            "id": 0
        }


@app.before_request
def prepare_session_and_csrf_check():
    if not "state" in login_session:
        init()
    csrf_protect()
    create_csrf_token()


#########################
# CSRF Security Methods #
#########################

def create_csrf_token():
    state = sha256(urandom(1024)).hexdigest()
    login_session["state"] = state


def csrf_protect():
    if request.method == "POST":
        token = login_session.pop('state', None)
        if not token or token != request.form.get('_csrf_token'):
            print("Token was {} but we expected {}".format(
                request.form.get("_csrf_token"), token
            ))
            abort(403)


def get_csrf_token():
    return login_session["state"]


##############################
# Google Authentication Code #
##############################

GoogleOAuthWrapper = GConnect(login_session)


@app.route("/gconnect")
def gconnect():
    code = request.args.get("code")
    # if state != login_session[""]:
    #    return "Error"
    try:
        GoogleOAuthWrapper.gconnect(code)
    except RuntimeError:
        return GoogleOAuthWrapper.response
    else:
        access_token = GoogleOAuthWrapper.access_token
        gplus_id = GoogleOAuthWrapper.gplus_id
        data = GoogleOAuthWrapper.data
        login_session["access_token"] = access_token
        login_session["gplus_id"] = gplus_id
        login_session["username"] = data["name"]
        login_session["email"] = data["email"]
        login_session["user_id"] = get_user_id(login_session["email"],
                                               create_user, login_session)
        return redirect(url_for("main_page"))


@app.route("/gdisconnect", methods=["POST"])
def gdisconnect():
    access_token = login_session["access_token"]
    user_token_revoked = GoogleOAuthWrapper.gdisconnect(access_token)
    if user_token_revoked:
        del login_session["access_token"]
        del login_session["gplus_id"]
        del login_session["username"]
        del login_session["email"]
        del login_session["user_id"]
        return redirect(url_for("main_page"))


####################
# JSON API methods #
####################

@app.route("/admin")
def print_session():
    """ Some means to make the Server state visible in browser """
    output = "{<br>"
    for x in login_session.__iter__():
        output += "    {}: {}<br>".format(x, login_session[x])
    output += "<br><br><br>"
    character = get_character_inventory()
    for x in character.__iter__():
        output += "    {}: {}<br>".format(x, character[x])
    itemDB.print_this()
    return output


@app.route("/api/skin/<int:skin_id>")
def list_all_categories(skin_id):
    skin = skinDB.filter(id=skin_id).one()
    return jsonify({part: getattr(skin, part).serialize() for part in body_parts})


@app.route("/api/item/<int:item_id>")
def show_item_detail(item_id):
    item = itemDB.filter(id=item_id).one()
    return jsonify(item.serialize())


@app.route("/api/inventory/<string:inv_name>/categories/")
def list_categories_of_inventory(inv_name):
    id = get_inventory_type_id_by_inventory_name(inv_name)
    categories = categoryDB.filter(inventory_type_id=id).all()
    return jsonify(item_categories=[c.serialize() for c in categories])


@app.route("/api/inventory/<string:inv_name>/items/")
def list_items_of_inventory(inv_name):
    id = get_inventory_type_id_by_inventory_name(inv_name)
    category_ids = categoryDB.session.query(Category.id).\
        filter(Category.inventory_type_id == id)
    items = itemDB.session.query(Item).filter(Item.category_id.in_(category_ids))
    return jsonify(items=[i.serialize() for i in items])


############################
# Main site and Skins #
############################

# Skins are a set of inventory items that were saved
# to form a specific set of clothes like a full body
# costume.


@app.route("/")
def main_page():
    skins = skinDB.read()
    character = get_character_inventory()
    return render_template(
        "main.html",
        skins=skins,
        character=character,
        session=login_session
    )


@app.route("/inventory/skin/<int:skin_id>")
def open_skin(skin_id):
    authenticated = load_item_ids_into_session_and_authenticate(skin_id)
    character = get_character_inventory()
    skins = skinDB.read()
    return render_template(
        "main.html",
        session=login_session,
        character=character,
        skins=skins,
        skin_id=skin_id,
        authenticated=authenticated
    )


def load_item_ids_into_session_and_authenticate(skin_id):
    item_set = skinDB.filter(id=skin_id).one()
    for body_part in body_parts:
        try:
            item_id = getattr(item_set, body_part).id
            login_session[body_part] = item_id
        except AttributeError:
            login_session[body_part] = 0
    return item_set.user_id == login_session["user_id"]


def get_character_inventory():
    """
    Gets Image and description for each bodw part
    according according to the login_session
    """
    return {body_part: get_item_info_by_body_part(body_part)
            for body_part in body_parts}


def get_item_info_by_body_part(body_part):
    item_id = login_session[body_part]
    item_info = item_or_default_item(item_id)
    return item_info


def item_or_default_item(item_id):
    if item_id == 0:
        return {
            "image": "default.png",
            "description": ""
        }
    item = itemDB.filter(id=item_id).one()
    return {
        "image": item.image,
        "description": item.description
    }


@app.route(
    "/inventory/skin/save", methods=["POST"])
def save_skin():
    current_skin = {body_part + "_id": login_session[body_part]
                    for body_part in body_parts}
    current_skin["user_id"] = login_session["user_id"]
    current_skin["title"] = request.form["name"]
    skinDB.add(**current_skin)
    return redirect(url_for("main_page"))


@app.route(
    "/inventory/skin/<int:skin_id>/delete", methods=["POST"])
def delete_skin(skin_id):
    delete_candidate = skinDB.filter(id=skin_id).one()
    if is_not_authenticated(delete_candidate.user_id):
        return "failure"
    skinDB.session.delete(delete_candidate)
    skinDB.session.commit()
    return "success"


##################
# Category Layer #
##################

@app.route("/inventory/<string:inv_name>/")
def show_inventory(inv_name):
    categories = get_categories_by_inventory_name(inv_name)
    return render_template(
        "inventory.html",
        session=login_session,
        inv_name=inv_name,
        categories=categories,
        items=[]
    )


@app.route("/inventory/<string:inv_name>/category/<int:category_id>/")
def show_category(inv_name, category_id):
    categories = get_categories_by_inventory_name(inv_name)
    items = get_items_by_category_id(category_id)
    item = get_item_by_item_id(request.args.get("item"))
    return render_template(
        "inventory.html",
        session=login_session,
        inv_name=inv_name,
        categories=categories,
        items=items,
        category_id=category_id,
        item=item
    )


################################
# Add, Edit, Delete Categories #
################################

@app.route(
    "/inventory/<string:inv_name>/category/new",
    methods=["POST"])
def add_category(inv_name):
    inventory_id = get_inventory_type_id_by_inventory_name(inv_name)
    category = categoryDB.add(
        name=request.form["name"],
        user_id=login_session["user_id"],
        inventory_type_id=inventory_id
    )
    flash("New Category {} added.".format(request.form["name"]))
    return redirect(url_for(
        "show_category", inv_name=inv_name, category_id=category.id))


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/edit",
    methods=["POST"])
def edit_category(inv_name, category_id):
    updates = filter_form(request.form, ["name"])
    category = categoryDB.filter(id=category_id).one()
    if is_not_authenticated(category.user_id):
        return
    categoryDB.update({"id": category_id}, updates)
    return redirect(url_for(
        "show_category", inv_name=inv_name, category_id=category_id))


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/delete",
    methods=["POST"])
def delete_category(inv_name, category_id):
    category = categoryDB.filter(id=category_id).one()
    if is_not_authenticated(category.user_id):
        return
    categoryDB.session.delete(category)
    categoryDB.session.commit()
    for item in get_items_by_category_id(category_id):
        itemDB.delete(id=item.id)
    return url_for(
        "show_inventory",
        inv_name=inv_name
    )


#####################
# Single Item Layer #
#####################

@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/" +
    "item/<int:item_id>/")
def show_item_details(inv_name, category_id, item_id):
    return redirect(
        "/inventory/{}/category/{}/?item={}".format(
            inv_name, category_id, item_id
        )
    )


###################################
# Equip, Create, Edit, Delete Item #
###################################

@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/" +
    "item/<int:item_id>/equip",
    methods=["POST"])
def equip_item(inv_name, category_id, item_id):
    login_session[inv_name] = item_id
    return url_for("main_page")


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/item/new",
    methods=["POST"])
def add_item(inv_name, category_id):
    form = filter_form(request.form, ["name", "image", "description"])
    try:
        form["image"] = get_and_store_picture(form["image"], inv_name)
    except IOError or ValueError:
        return redirect(url_for(
            "show_category",
            inv_name=inv_name,
            category_id=category_id
        ))
    item = insert_new_item_to_database(form, category_id)
    return redirect(url_for(
        "show_item_details",
        inv_name=inv_name,
        category_id=category_id,
        item_id=item.id
    ))


def get_and_store_picture(url, inv_name):
    name = "{}.png".format(str(uuid4()))
    file_path = "./static/img/{}/{}".format(inv_name, name)
    px = PictureResizer()
    px.pixelate_url(url, file_path)
    return name


def insert_new_item_to_database(form, category_id):
    form["category_id"] = category_id
    form["user_id"] = login_session["user_id"]
    return itemDB.add(**form)


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/"
    "item/<int:item_id>/edit",
    methods=["POST"])
def edit_item(inv_name, category_id, item_id):
    updates = filter_form(request.form, ["name", "description"])
    item = itemDB.filter(id=item_id).one()
    if is_not_authenticated(item.user_id):
        return
    itemDB.update({"id": item_id}, updates)
    return redirect(url_for(
        "show_item_details",
        inv_name=inv_name,
        category_id=category_id,
        item_id=item_id
    ))


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/" +
    "item/<int:item_id>/delete",
    methods=["POST"])
def delete_item(inv_name, category_id, item_id):
    item = itemDB.filter(id=item_id).one()
    if is_not_authenticated(item.user_id):
        return
    item_name = get_item_by_item_id(item_id).image
    remove_picture("img/{}/{}".format(inv_name, item_name))
    remove_item_from_skins(inv_name, item_id)
    remove_item_from_session(inv_name, item_id)
    itemDB.delete(id=item_id)
    return url_for(
        "show_category",
        inv_name=inv_name,
        category_id=category_id
    )


def remove_picture(path):
    remove("./" + url_for(
        "static", filename=path))


def remove_item_from_skins(inv_name, item_id):
    inv_id = "{}_id".format(inv_name)
    skins_with_said_item = skinDB.session.query(Skin).filter(
        getattr(Skin, inv_id) == item_id
    ).all()
    for skin in skins_with_said_item:
        setattr(skin, inv_id, 0)
    skinDB.session.commit()


def remove_item_from_session(inv_name, item_id):
    if login_session[inv_name] == item_id:
        login_session[inv_name] = 0


##################
# Util functions #
##################

# useful queries

def get_inventory_type_id_by_inventory_name(inv_name):
    return inventoryDB.filter(
        name=inv_name
    ).one().id


def get_categories_by_inventory_name(inv_name):
    id = get_inventory_type_id_by_inventory_name(inv_name)
    return categoryDB.filter(
        inventory_type_id=id
    ).all()


def get_items_by_category_id(category_id):
    return itemDB.filter(
        category_id=category_id
    ).all()


def get_item_by_item_id(item_id):
    if not item_id:
        return None
    else:
        return itemDB.filter(
            id=item_id
        ).one()


# user handling

def is_not_authenticated(user_id):
    return user_id != login_session["user_id"]


def get_user_id(email, callback, input):
    try:
        user = userDB.filter(email=email).one()
        return user.id
    except NoResultFound:
        return callback(input)


def create_user(login_session):
    userDB.add(
        name=login_session["username"],
        email=login_session["email"]
    )
    user = userDB.filter(email=login_session["email"]).one()
    return user.id


# misc

def filter_form(form, keys):
    return {key: form[key] for key in keys}


if __name__ == "__main__":
    app.secret_key = sha256(urandom(2048)).hexdigest()

    app.jinja_env.globals['csrf_token'] = get_csrf_token
    app.debug = True
    app.run(host="0.0.0.0", port=5000)