
# Ultimate Inventory

These are the source files for a protoypal web application based on Flask 0.12.2. 
Obviously inspirated by RPGs like Diablo, the user is able to create his own categories
and items in that category. He can then use these items as equipment and save the charcter 
skins created that way.

## Setup

To install execute `pip install requirements.txt` within the folder to install the required
Python packages. To create the database and fill it with sample data, run 
```
pip install requirements.txt
python utils/
python utils/flood_database.py
```
Then run the app locally by typing
`python project.py` and point your browser to [localhost:5000](localhost:5000/)

## Tests

Sadly no Unittests but one may test the api quickly by running `python utils/testAPI.py`
