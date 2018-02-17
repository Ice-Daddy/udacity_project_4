from flask import Flask, render_template, request, redirect,\
    jsonify, url_for, flash
from utils.GoogleConnect import GConnect
from utils.database_interact import DBInteractor
from utils.database_init import InventoryType, Category, Item, User
from flask import session as login_session

app = Flask(__name__)

# Database operation Helpers


inventoryDB = DBInteractor(InventoryType)
categoryDB = DBInteractor(Category)
userDB = DBInteractor(User)
itemDB = DBInteractor(Item)


##############################
# Google Authentication Code #
##############################

GoogleOAuthWrapper = GConnect(login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    try:
        GoogleOAuthWrapper.gconnect(request)
    except RuntimeError as errormessage:
        return errormessage
    else:
        access_token = GoogleOAuthWrapper.access_token
        gplus_id = GoogleOAuthWrapper.gplus_id
        data = GoogleOAuthWrapper.get_user_data_from_google()
        login_session['access_token'] = access_token
        login_session['gplus_id'] = gplus_id
        login_session['username'] = data['name']
        login_session['email'] = data['email']
        login_session['user_id'] = getUserID(login_session['email'],
                                             createUser, login_session)
        return "Success"


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    user_token_revoked = GoogleOAuthWrapper.gdisconnect(access_token)
    if (user_token_revoked):
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']


####################
# JSON API methods #
####################


@app.route('/api/inventory/')
def list_inventory_types():
    inventory_types = inventoryDB.read()
    return jsonify(inventory_types=[i.serialize for i in inventory_types])


@app.route('/api/inventory/<int:inventory_id>/categories/')
def list_categories(inventory_id):
    categories = categoryDB.filter(inventory_type_id=inventory_id).all()
    return jsonify(item_categories=[c.serialize for c in categories])


@app.route('/api/inventory/<int:inventory_id>/category/<int:category_id>/')
def list_items_of_category(inventory_id, category_id):
    category = categoryDB.filter(id=category_id).one()
    return jsonify(restaurants=[c.serialize for c in category])


############################
# Main site and categories #
############################


@app.route('/')
@app.route('/inventory/')
def main_page():
    if 'username' in login_session:
        html = 'restaurants.html'
    else:
        html = 'publicRestaurant.html'
    return "Main Page"


################################
# Add, Edit, Delete Categories #
################################


@app.route(
    '/inventory/<int:inventory_id>/category/new',
    methods=['GET', 'POST']
)
def new_category(inventory_id):
    if 'username' not in login_session:
        flash("You need to be logged in")
    return "New Category Page"


@app.route(
    '/inventory/<int:inventory_id>/category/<int:category_id>/edit',
    methods=['GET', 'POST'])
def edit_category(inventory_id, category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        pass
    else:
        return "Edit Category Page"


@app.route(
    '/inventory/<int:inventory_id>/category/<int:category_id>/delete',
    methods=['GET', 'POST'])
def delete_category(inventory_id, category_id):
    if 'username' not in login_session:
        return redirect('/')
    if request.method == 'POST':
        pass
    else:
        return "Detlete Gategory Page"


#####################
# Single Item Layer #
#####################


@app.route(
    '/inventory/<int:inventory_id>\
        /category/<int:category_id>/item/<int:item_id>/'
)
def show_item_details(inventory_id, category_id, item_id):
    return "Show Items Page"


#############################
# Create, Edit, Delete Item #
#############################


@app.route(
    '/inventory/<int:inventory_id>\
        /category/<int:category_id>/item/new',
    methods=['GET', 'POST'])
def new_item(inventory_id, category_id):
    if 'username' not in login_session:
        return redirect('/')
    if request.method == 'POST':
        pass
    else:
        return "Create Item Page"


# Edit a menu item


@app.route(
    '/inventory/<int:inventory_id>\
        /category/<int:category_id>/item/<int:item_id>/edit',
    methods=['GET', 'POST'])
def editItem(inventory_id, category_id, item_id):
    if 'username' not in login_session:
        return redirect('/')
    if request.method == 'POST':
        pass
    else:
        return "Edit Item Page"


# Delete a menu item
@app.route(
    '/inventory/<int:inventory_id>\
        /category/<int:category_id>/item/<int:item_id>/new',
    methods=['GET', 'POST'])
def deleteItem(inventory_id, category_id, item_id):
    if 'username' not in login_session:
        return redirect('/')
    if request.method == 'POST':
        pass
    else:
        return "Delete Item Page"


def getUserID(email, callback, input):
    try:
        user = userDB.filter(email=email).one()
        return user.id
    except:
        return callback(input)


def getUserInfo(user_id):
    return userDB.filter(id=user_id).one()


def createUser(login_session):
    userDB.add(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    user = userDB.filter(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)