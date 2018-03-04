
from flask import Flask, render_template, request, redirect,\
    jsonify, flash, url_for  # make_response
from sqlalchemy.orm.exc import NoResultFound
import hashlib
import os
from utils.GoogleConnect import GConnect
from utils.database_interact import DBInteractor
from utils.database_init import InventoryType, Category, Item, User, Skin
from flask import session as login_session

app = Flask(__name__)

# Database operation Helpers


inventoryDB = DBInteractor(InventoryType)
categoryDB = DBInteractor(Category)
userDB = DBInteractor(User)
itemDB = DBInteractor(Item)
skinDB = DBInteractor(Skin)


def create_csrf_token():
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    login_session['state'] = state


##############################
# Google Authentication Code #
##############################

GoogleOAuthWrapper = GConnect(login_session)


@app.route('/gconnect')
def gconnect():
    code = request.args.get('code')
    # if state != login_session['']:
    #    return "Error"
    try:
        GoogleOAuthWrapper.gconnect(code)
    except RuntimeError:
        return GoogleOAuthWrapper.response
    else:
        access_token = GoogleOAuthWrapper.access_token
        gplus_id = GoogleOAuthWrapper.gplus_id
        data = GoogleOAuthWrapper.data
        login_session['access_token'] = access_token
        login_session['gplus_id'] = gplus_id
        login_session['username'] = data['name']
        login_session['email'] = data['email']
        login_session['user_id'] = getUserID(login_session['email'],
                                             createUser, login_session)
        return redirect(url_for("main_page"))


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    access_token = login_session['access_token']
    user_token_revoked = GoogleOAuthWrapper.gdisconnect(access_token)
    if (user_token_revoked):
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        return redirect(url_for('main_page'))


####################
# JSON API methods #
####################


@app.route('/api/inventory/')
def list_inventory_types():
    inventory_types = inventoryDB.read()
    return jsonify(inventory_types=[i.serialize for i in inventory_types])


@app.route('/api/inventory/<string:inventory_id>/categories/')
def list_categories(inventory_id):
    categories = categoryDB.filter(inventory_type_id=inventory_id).all()
    return jsonify(item_categories=[c.serialize for c in categories])


@app.route('/api/inventory/<string:inventory_id>/category/<int:category_id>/')
def list_items_of_category(inventory_id, category_id):
    category = categoryDB.filter(id=category_id).one()
    return jsonify(restaurants=[c.serialize for c in category])

############################
# Main site and categories #
############################


@app.route('/')
def main_page():
    create_csrf_token()
    skins = skinDB.read()
    return render_template(
        "main.html",
        session=login_session,
        skins=skins,
        images=login_session
    )
    

@app.route('/inventory/')
def main_page_with_skin():
    create_csrf_token()
    skin_id = request.args.get('skin')
    images = get_images_by_skin_id(skin_id)
    skins = skinDB.read()
    return render_template(
        "main.html",
        session=login_session,
        skins=skins,
        images=images
    )


def get_images_by_skin_id(skin_id):
    body_parts = ["head", "torso", "legs", "hands", "feet",
                  "left_hand", "right_hand", "companion"]
    item_set = skinDB.filter(id=skin_id).one()
    d = dict()
    for body_part in body_parts:
        img_file = getattr(item_set, body_part).image
        if img_file:
            d[body_part] = img_file
        else:
            d[body_part] = 'default.png'
    return d

################################
# Add, Edit, Delete Categories #
################################


@app.route('/inventory/<string:inventory_id>/')
def show_inventory(inventory_id):
    create_csrf_token()
    categories = get_categories_by_inventory_id(inventory_id)
    return render_template(
        "inventory.html",
        session=login_session,
        inventory_id=inventory_id,
        categories=categories,
        items=[]
    )


@app.route('/inventory/<string:inventory_id>/category/<int:category_id>/')
def show_category(inventory_id, category_id):
    create_csrf_token()
    if 'username' not in login_session:
        flash("You need to be logged in")
    item = request.args.get('item')
    categories = get_categories_by_inventory_id(inventory_id)
    items = get_items_by_category_id(category_id)
    if item:
        item = get_item_by_item_id(item)
    return render_template(
        'inventory.html',
        session=login_session,
        inventory_id=inventory_id,
        item=item,
        categories=categories,
        items=items
    )


@app.route(
    '/inventory/<string:inventory_id>/category/new',
    methods=['POST'])
def new_category(inventory_id):
    ctgry = categoryDB.add(
        name=request.form['name'],
        inventory_type_id=inventory_id,
    )
    flash("New Category {} added.".format(request.form['name']))
    return redirect(url_for(
        'show_category', inventory_id=inventory_id, category_id=ctgry.id
    ))


@app.route(
    '/inventory/<string:inventory_id>/category/<int:category_id>/edit',
    methods=['POST'])
def edit_category(inventory_id, category_id):
    updates = parse_form(request.form)
    categoryDB.update({"id": "category_id"}, updates)
    return redirect(url_for(
        'show_category', inventory_id=inventory_id, category_id=category_id
    ))


@app.route(
    '/inventory/<string:inventory_id>/category/<int:category_id>/delete',
    methods=['POST'])
def delete_category(inventory_id, category_id):
    categoryDB.delete(id=category_id)
    return redirect(url_for(
        'show_inventory',
        inventory_id=inventory_id
    ))

#####################
# Single Item Layer #
#####################


@app.route(
    "/inventory/<string:inventory_id>\
        /category/<int:category_id>/item/<int:item_id>/"
)
def show_item_details(inventory_id, category_id, item_id):
    return redirect(
        "/inventory/{}/category/{}/item?item={}".format(
            inventory_id, category_id, item_id
        )
    )

#############################
# Create, Edit, Delete Item #
#############################


@app.route(
    '/inventory/<string:inventory_id>\
        /category/<int:category_id>/item/new',
    methods=['POST'])
def new_item(inventory_id, category_id):
    form = parse_form(request.form)
    form.category_id = category_id
    form.user_id = login_session["user_id"]
    item = itemDB.add(**form)
    return redirect(url_for(
        'show_item_details',
        inventory_id=inventory_id,
        category_id=category_id,
        item_id=item.id
    ))


@app.route(
    '/inventory/<string:inventory_id>\
        /category/<int:category_id>/item/<int:item_id>/edit',
    methods=['POST'])
def editItem(inventory_id, category_id, item_id):
    updates = parse_form(request.form)
    itemDB.update({'id': item_id}, updates)
    return redirect(url_for(
        'show_item_details',
        inventory_id=inventory_id,
        category_id=category_id,
        item_id=item_id
    ))


@app.route(
    '/inventory/<string:inventory_id>\
        /category/<int:category_id>/item/<int:item_id>/new',
    methods=['POST'])
def deleteItem(inventory_id, category_id, item_id):
    itemDB.delete(id=item_id)
    return redirect(url_for(
        'show_category',
        inventory_id=inventory_id,
        category_id=category_id
    ))

##################
# Util functions #
##################


def get_categories_by_inventory_id(inventory_id):
    return categoryDB.filter(
        name=inventory_id
    ).all()


def get_items_by_category_id(category_id):
    return itemDB.filter(
        category_id=category_id
    ).all()


def get_item_by_item_id(item_id):
    return itemDB.filter(
        item_id=item_id
    ).one()


def parse_form(form):
    return {field: entry
            for field, entry in form.iteritems() if entry}


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
        name=login_session['username'],
        email=login_session['email']
    )
    user = userDB.filter(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
