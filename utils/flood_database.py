from database_interact import DBInteractor
from database_init import InventoryType, Category, Item, User


if __name__ == '__main__':
    inventoryDB = DBInteractor(InventoryType)
    categoryDB = DBInteractor(Category)
    itemDB = DBInteractor(Item)
    userDB = DBInteractor(User)

    inventory_types = [
        {
            'name': 'Head'
        },
        {
            'name': 'Torso'
        },
        {
            'name': 'Legs'
        },
        {
            'name': 'Hands'
        },
    ]

    users = [
        {
            'name': 'Moritz Vetter',
            'email': 'moritz.vetter@gmx.de'
        }
    ]

    categories = [
        {
            'name': 'Helmets',
            'description': 'Owned by all cultures that were \
            lucky enough to stumble across iron, nothing \
            protects your beloved marbles and fashionable \
            hairline like an upside down brass cup.',
            'inventory_type_id' : 1
        },
        {
            'name': 'Shirts',
            'description': 'Owned by all cultures that were \
            lucky enough to stumble across iron, nothing \
            protects your beloved marbles and fashionable \
            hairline like an upside down brass cup.',
            'inventory_type_id' : 2
        },
        {
            'name': 'pants',
            'description': 'Owned by all cultures that were \
            lucky enough to stumble across iron, nothing \
            protects your beloved marbles and fashionable \
            hairline like an upside down brass cup.',
            'inventory_type_id' : 3
        },
        {
            'name': 'gloves',
            'description': 'Owned by all cultures that were \
            lucky enough to stumble across iron, nothing \
            protects your beloved marbles and fashionable \
            hairline like an upside down brass cup.',
            'inventory_type_id' : 4
        }
    ]

    items = [
        {
            'name': 'Wikinger helmet',
            'description': 'Was worn by Wikings',
            'image': 'helmet.png',
            'ATK': 2,
            'DEF': 14,
            'category_id': 1,
            'user_id': 1
        },
        {
            'name': 'Fashionable Glitter Shirt',
            'description': 'Was worn by Wikings',
            'image': 'shirt.png',
            'ATK': 1,
            'DEF': 3,
            'category_id': 2,
            'user_id': 1
        },
        {
            'name': 'Wikinger pants',
            'description': 'Was worn by Wikings',
            'image': 'pants.png',
            'ATK': 0,
            'DEF': 6,
            'category_id': 3,
            'user_id': 1
        },
        {
            'name': 'Wikinger gloves',
            'description': 'Was worn by Wikings',
            'image': 'gloves.png',
            'ATK': 2,
            'DEF': 3,
            'category_id': 4,
            'user_id': 1
        },
    ]

    for iType in inventory_types:
        inventoryDB.add(**iType)

    for user in users:
        userDB.add(**user)

    for category in categories:
        categoryDB.add(**category)

    for item in items:
        itemDB.add(**item)