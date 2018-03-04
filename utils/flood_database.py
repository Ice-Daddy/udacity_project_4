from database_interact import DBInteractor
from database_init import InventoryType, Category, Item, User, Skin


if __name__ == '__main__':
    inventoryDB = DBInteractor(InventoryType)
    categoryDB = DBInteractor(Category)
    itemDB = DBInteractor(Item)
    userDB = DBInteractor(User)
    skinDB = DBInteractor(Skin)

    inventory_types = [
        {
            'name': 'head'
        },
        {
            'name': 'torso'
        },
        {
            'name': 'legs'
        },
        {
            'name': 'hands'
        },
        {
            'name': 'feet'
        },
        {
            'name': 'right_hand'
        },
        {
            'name': 'left_hand'
        },
        {
            'name': 'Companion'
        }
    ]

    users = [
        {
            'name': 'Moritz Vetter',
            'email': 'moritz.vetter@gmx.de'
        }
    ]

    categories = [
        {
            'name': 'Historical Helmets',
            'inventory_type_id': 1
        },
        {
            'name': 'T-shirts',
            'inventory_type_id': 2
        },
        {
            'name': '80s',
            'inventory_type_id': 3
        },
        {
            'name': 'Winter Gloves',
            'inventory_type_id': 4
        },
        {
            'name': 'Sport shoes',
            'inventory_type_id': 5
        },
        {
            'name': 'Tools',
            'inventory_type_id': 6
        },
        {
            'name': 'Instruments',
            'inventory_type_id': 7
        },
        {
            'name': 'Pokemon',
            'inventory_type_id': 8
        }
    ]

    items = [
        {
            'name': 'Viking helmet',
            'description': 'Was worn by Vikings - as their bloody booty',
            'image': 'viking_helmet.png',
            'category_id': 1
        },
        {
            'name': 'Medieval helmet',
            'description': 'Was worn by Vikings - as their bloody booty',
            'image': 'medieval_helmet.png',
            'category_id': 1
        },
        {
            'name': 'Simple Leather helmet',
            'description': 'Was worn by Vikings - as their bloody booty',
            'image': 'simple_leather_helmet.png',
            'category_id': 1
        },
        {
            'name': 'Heavy Metal Shirt',
            'description': 'Was worn by Vikings',
            'image': 'metal_shirt.png',
            'category_id': 2
        },
        {
            'name': 'Pink T-Shirt',
            'description': 'Was worn by Vikings',
            'image': 'pink_t-shirt.png',
            'category_id': 2
        },
        {
            'name': 'Sweat Soaked Shirt',
            'description': 'Was worn by Vikings',
            'image': 'sweat_soaked_shirt.png',
            'category_id': 2
        },
        {
            'name': 'Groovy glittery pants',
            'description': 'Was not worn by Vikings',
            'image': 'groovy_glittery_pants.png',
            'category_id': 3
        },
        {
            'name': 'Ripped Jeans',
            'description': 'Was not worn by Vikings',
            'image': 'ripped_jeans.png',
            'category_id': 3
        },
        {
            'name': 'Leather Punk Pants',
            'description': 'Was not worn by Vikings',
            'image': 'leather_punk_pants.png',
            'category_id': 3
        },
        {
            'name': "Grandmother's hand-knit gloves",
            'description': 'Vikings had gloves and grandmothers so why not?',
            'image': 'hand_knit_gloves.png',
            'category_id': 4
        },
        {
            'name': "Red Gloves",
            'description': 'Vikings had gloves and grandmothers so why not?',
            'image': 'red_gloves.png',
            'category_id': 4
        },
        {
            'name': "Metal Gloves",
            'description': 'Vikings had gloves and grandmothers so why not?',
            'image': 'metal_gloves.png',
            'category_id': 4
        },
        {
            'name': "Tennis shoes",
            'description': 'Was worn by sporty, snobby Vikings',
            'image': 'tennis_shoes.png',
            'category_id': 5
        },
        {
            'name': "Scooberdiver shoes",
            'description': 'Was worn by sporty, snobby Vikings',
            'image': 'scooberdiver_shoes.png',
            'category_id': 5
        },
        {
            'name': "Running shoes",
            'description': 'Was worn by sporty, snobby Vikings',
            'image': 'running_shoes.png',
            'category_id': 5
        },
        {
            'name': "Screwdriver",
            'description': 'Was not worn by Vikings',
            'image': 'screwdriver.png',
            'category_id': 6
        },
        {
            'name': "Spade",
            'description': 'Was not worn by Vikings',
            'image': 'spade.png',
            'category_id': 6
        },
        {
            'name': "Hacksaw",
            'description': 'Was not worn by Vikings',
            'image': 'hacksaw.png',
            'category_id': 6
        },
        {
            'name': "Trombone",
            'description': 'Pales in the face of the mighty Viking war horn',
            'image': 'trombone.png',
            'category_id': 7
        },
        {
            'name': "Triangle",
            'description': 'Pales in the face of the mighty Viking war horn',
            'image': 'triangle.png',
            'category_id': 7
        },
        {
            'name': "Tambourine",
            'description': 'Pales in the face of the mighty Viking war horn',
            'image': 'tambourine.png',
            'category_id': 7
        },
        {
            'name': 'Pikachu',
            'description': 'Cuuuuuuuute! <3<3<3',
            'image': 'pikachu.png',
            'category_id': 8
        },
        {
            'name': 'Raichu',
            'description': 'Cuuuuuuuute! <3<3<3',
            'image': 'raichu.png',
            'category_id': 8
        },
        {
            'name': 'charmander',
            'description': 'Cuuuuuuuute! <3<3<3',
            'image': 'charmander.png',
            'category_id': 8
        }
    ]

    skins = [
        {
            "title": "Test skin 1",
            "head_id": 1,
            "torso_id": 4,
            "legs_id": 7,
            "hands_id": 10,
            "feet_id": 13,
            "left_hand_id": 16,
            "right_hand_id": 19,
            "companion_id": 22
        },
        {
            "title": "Test skin 2",
            "head_id": 2,
            "torso_id": 5,
            "legs_id": 8,
            "hands_id": 11,
            "feet_id": 14,
            "left_hand_id": 17,
            "right_hand_id": 20,
            "companion_id": 23
        },
        {
            "title": "Test skin 3",
            "head_id": 3,
            "torso_id": 6,
            "legs_id": 9,
            "hands_id": 12,
            "feet_id": 15,
            "left_hand_id": 18,
            "right_hand_id": 21,
            "companion_id": 24
        }
    ]

    for iType in inventory_types:
        inventoryDB.add(**iType)

    for user in users:
        userDB.add(**user)

    for category in categories:
        categoryDB.add(**category)

    for item in items:
        itemDB.add(**item)

    for skin in skins:
        skinDB.add(**skin)