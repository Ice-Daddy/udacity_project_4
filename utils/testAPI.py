from urllib2 import urlopen

HOST_NAME = "http://localhost:5000/api"

SKIN_ID = "2"
ITEM_ID = "5"
INVENTORY_ID = "torso"

TEST_API1 = "{}/skin/{}".format(HOST_NAME, SKIN_ID)
TEST_API2 = "{}/item/{}".format(HOST_NAME, ITEM_ID)
TEST_API3 = "{}/inventory/{}/categories/".format(HOST_NAME, INVENTORY_ID)
TEST_API4 = "{}/inventory/{}/items/".format(HOST_NAME, INVENTORY_ID)

apis = [
    TEST_API1,
    TEST_API2,
    TEST_API3,
    TEST_API4
]

for api in apis:
    print "Pinging API endpoint " + api
    print urlopen(api).read()
