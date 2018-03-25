
from flask import Flask, render_template, request, redirect,\
    jsonify, flash, url_for, session as login_session
from sqlalchemy.orm.exc import NoResultFound
from hashlib import sha256
from os import urandom, remove
from uuid import uuid4

from utils.pixelate import Pixelator
from utils.GoogleConnect import GConnect
from utils.database_interact import DBInteractor
from utils.database_init import InventoryType, Category, Item, User, Skin

app = Flask(__name__)

# Database operation Helpers


inventoryDB = DBInteractor(InventoryType)
categoryDB = DBInteractor(Category)
userDB = DBInteractor(User)
itemDB = DBInteractor(Item)
skinDB = DBInteractor(Skin)

body_parts = ["head", "torso", "legs", "hands", "feet",
              "left_hand", "right_hand", "companion"]


def create_csrf_token():
    if not login_session.get("state"):
        for part in body_parts:
            login_session[part] = 0
    state = sha256(urandom(1024)).hexdigest()
    login_session["state"] = state


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
        login_session["user_id"] = getUserID(login_session["email"],
                                             createUser, login_session)
        return redirect(url_for("main_page"))


@app.route("/gdisconnect", methods=["POST"])
def gdisconnect():
    access_token = login_session["access_token"]
    user_token_revoked = GoogleOAuthWrapper.gdisconnect(access_token)
    if (user_token_revoked):
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
    create_csrf_token()
    output = "{<br>"
    for x in login_session.__iter__():
        output += "    {}: {}<br>".format(x, login_session[x])
    output += "<br><br><br>"
    character = get_character_inventory()
    for x in character.__iter__():
        output += "    {}: {}<br>".format(x, character[x])
    itemDB.print_this()
    return output


@app.route("/api/all_categories/")
def list_all_categories():
    categories = categoryDB.read()
    return jsonify({c.id: c.serialize() for c in categories})


@app.route("/api/all_items/")
def list_all_items():
    items = itemDB.read()
    return jsonify({i.id: i.serialize() for i in items})


@app.route("/api/inventory/<string:inv_name>/categories/")
def list_categories_of_inventory(inv_name):
    id = get_inventory_type_id_by_inventory_name(inv_name)
    categories = categoryDB.filter(inventory_type_id=id).all()
    return jsonify(item_categories=[c.serialize() for c in categories])


@app.route("/api/inventory/<string:inv_name>/items/")
def list_items_of_inventory(inv_name):
    id = get_inventory_type_id_by_inventory_name(inv_name)
    print(id)
    category_ids = categoryDB.session.query(Category.id).\
        filter(Category.inventory_type_id == id)
    print(category_ids)
    items = itemDB.session.query(Item).filter(Item.category_id.in_(category_ids))
    return jsonify(items=[i.serialize() for i in items])


@app.route("/api/inventory/<string:inv_name>/category/<int:category_id>/")
def list_items_of_category(inv_name, category_id):
    items = itemDB.filter(category_id=category_id).all()
    return jsonify(items=[i.serialize() for i in items])


############################
# Main site and categories #
############################

@app.route("/")
def main_page():
    create_csrf_token()
    skins = skinDB.read()
    character = get_character_inventory()
    return render_template(
        "main.html",
        skins=skins,
        character=character,
        session=login_session
    )


###########################
# Create and Delete Skins #
###########################

@app.route("/inventory/skin/<int:skin_id>")
def open_skin(skin_id):
    create_csrf_token()
    get_images_by_skin_id(skin_id)
    character = get_character_inventory()
    skins = skinDB.read()
    return render_template(
        "main.html",
        session=login_session,
        character=character,
        skins=skins,
        skin_id=skin_id
    )


@app.route(
    "/inventory/skin/save", methods=["POST"])
def save_skin():
    current_skin = {body_part + "_id": login_session[body_part]
                    for body_part in body_parts}
    current_skin["user_id"] = 1 #TODO login_session["user_id"]
    current_skin["title"] = request.form["name"]
    skinDB.add(**current_skin)
    return redirect(url_for("main_page"))


@app.route(
    "/inventory/skin/<int:skin_id>/delete", methods=["POST"])
def delete_skin(skin_id):
    skinDB.delete(id=skin_id)
    return "success"


def get_current_skin():
    return {body_part: login_session[body_part]
            for body_part in body_parts}


def get_character_inventory():
    return {body_part: get_item_info_by_body_part(body_part)
            for body_part in body_parts}


def get_item_info_by_body_part(body_part):
    id = login_session[body_part]
    item_info = item_or_default_item(id)
    return item_info


def item_or_default_item(id):
    print(id)
    if id == 0:
        return {
            "image": "default.png",
            "description": ""
        }
    item = itemDB.filter(id=id).one()
    return {
        "image": item.image,
        "description": item.description
    }


def get_images_by_skin_id(skin_id):
    item_set = skinDB.filter(id=skin_id).one()
    for body_part in body_parts:
        try:
            id = getattr(item_set, body_part).id
            login_session[body_part] = id
        except AttributeError:
            login_session[body_part] = 0
    print(login_session)


################################
# Add, Edit, Delete Categories #
################################

@app.route("/inventory/<string:inv_name>/")
def show_inventory(inv_name):
    create_csrf_token()
    categories = get_categories_by_inventory_name(inv_name)
    authorized = get_authorized_entities(categories)
    return render_template(
        "inventory.html",
        session=login_session,
        inv_name=inv_name,
        categories=categories,
        authorized=authorized,
        items=[]
    )


@app.route("/inventory/<string:inv_name>/category/<int:category_id>/")
def show_category(inv_name, category_id):
    create_csrf_token()
    categories = get_categories_by_inventory_name(inv_name)
    items = get_items_by_category_id(category_id)
    item = get_item_by_item_id(request.args.get("item"))
    authorized = get_authorized_entities(categories, items)
    return render_template(
        "inventory.html",
        category_id=category_id,
        session=login_session,
        inv_name=inv_name,
        item=item,
        categories=categories,
        items=items,
        authorized=authorized
    )


@app.route(
    "/inventory/<string:inv_name>/category/new",
    methods=["POST"])
def add_category(inv_name):
    inventory_id = get_inventory_type_id_by_inventory_name(inv_name)
    ctgry = categoryDB.add(
        name=request.form["name"],
        user_id=1, #TODO login_session["user_id"]
        inventory_type_id=inventory_id
    )
    flash("New Category {} added.".format(request.form["name"]))
    return redirect(url_for(
        "show_category", inv_name=inv_name, category_id=ctgry.id))


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/edit",
    methods=["POST"])
def edit_category(inv_name, category_id):
    updates = filter_form(request.form)
    categoryDB.update({"id": category_id}, updates)
    return redirect(url_for(
        "show_category", inv_name=inv_name, category_id=category_id))


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/delete",
    methods=["POST"])
def delete_category(inv_name, category_id):
    categoryDB.delete(id=category_id)
    for item in get_items_by_category_id(category_id):
        itemDB.delete(id=item.id)
    return url_for(
        "show_inventory",
        inv_name=inv_name
    )

def get_authorized_entities(categories, items=[]):
    user_id = login_session.get("user_id")
    authorized_categories = [c.id for c in categories
                              if c.user_id == user_id]
    authorized_items = [i.id for i in items
                              if i.user_id == user_id]
    return {
        "categories": authorized_categories,
        "items": authorized_items
    }

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
    image = itemDB.filter(id=item_id).one().image
    login_session[inv_name] = item_id
    return url_for("main_page")


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/item/new",
    methods=["POST"])
def add_item(inv_name, category_id):
    form = filter_form(request.form)
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


def insert_new_item_to_database(form, category_id):
    form["category_id"] = category_id
    form["user_id"] = 1 #TODO login_session["user_id"]
    return itemDB.add(**form)


def get_and_store_picture(url, inv_name):
    name = "{}.png".format(str(uuid4()))
    filename = "img/{}/{}".format(inv_name, name)
    add_new_picture(url, url_for("static", filename=filename))
    return name


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/"
    "item/<int:item_id>/edit",
    methods=["POST"])
def edit_item(inv_name, category_id, item_id):
    updates = filter_form(request.form)
    itemDB.update({"id": item_id}, updates)
    return url_for(
        "show_item_details",
        inv_name=inv_name,
        category_id=category_id,
        item_id=item_id
    )


@app.route(
    "/inventory/<string:inv_name>/category/<int:category_id>/" +
    "item/<int:item_id>/delete",
    methods=["POST"])
def delete_item(inv_name, category_id, item_id):
    print("Delete Item with ID " + str(item_id))
    item_name = get_item_by_item_id(item_id).image
    remove_picture("img/{}/{}".format(inv_name, item_name))
    remove_item_from_skins(inv_name, item_id)
    itemDB.delete(id=item_id)
    return url_for(
        "show_category",
        inv_name=inv_name,
        category_id=category_id
    )


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


# picture handling

px = Pixelator()


def add_new_picture(url, path):
    px.pixelate_url(url, "./" + path)


def remove_picture(path):
    remove("./" + url_for(
        "static", filename=path))


def remove_item_from_skins(inv_name, item_id):
    inv_id = "{}_id".filter(inv_name)
    skinDB.session.query(Skin).filter(
        getattr(Skin, inv_id) == item_id
    ).update({inv_id: 0})


# user handling

def getUserID(email, callback, input):
    try:
        user = userDB.filter(email=email).one()
        return user.id
    except NoResultFound:
        return callback(input)


def getUserInfo(user_id):
    return userDB.filter(id=user_id).one()


def createUser(login_session):
    userDB.add(
        name=login_session["username"],
        email=login_session["email"]
    )
    user = userDB.filter(email=login_session["email"]).one()
    return user.id


# misc

def filter_form(form):
    return {field: entry
            for field, entry in form.iteritems() if entry}


if __name__ == "__main__":
    app.secret_key = """\x17\x9a\xf7\x8a\xbe\x90\xe6T\xa6\x80
    \x84\x04)\x81\xef\xee"\xee\x84\xeeuE\x9bO\x92Y\x13F\x92{u
    \xc8\x0f\xf3E\x1c\"`J\xe4=k\x12\x17Ko\x0b\x7fL0#9iF4a1"""
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
