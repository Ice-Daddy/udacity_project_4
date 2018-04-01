
# Ultimate Inventory

These are the source files for a protoypal web application based on Flask 0.12.2. 
Obviously inspirated by RPGs like Diablo, the user is able to create his own categories
and items in that category. He can then use these items as equipment and save the charcter 
skins created that way.

## Setup

This application only works with Python2 because urllib2 is a requirement.

To install dependencies, execute `pip install requirements.txt` within the folder to install the required
Python packages. Then run the following two commands.
```
python utils/pixelate.py
python utils/flood_database.py
```
They will prepare the database and download pictures that will be used for the Prototype

Then run the app locally by typing
`python project.py` and point your browser to [localhost:5000](localhost:5000/)

## Tests

Sadly no Unittests - but one may test the api quickly by running `python utils/testAPI.py`
