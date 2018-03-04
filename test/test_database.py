"""
Test utils.database_interact.py
"""

import unittest
from utils.database_interact import DBInteractor
from utils.database_init import InventoryType


class TestDBInteractor(unittest.TestCase):

    inventoryDB = DBInteractor(InventoryType, 'sqlite:///TEST-DB.db')

    def test_read(self):
        self.assertEqual(type(self.inventoryDB.read()), type([])) 

    def test_add(self):
        original_length = len(self.inventoryDB.read())
        self.inventoryDB.add(name="testInventory")
        self.assertEqual(len(self.inventoryDB.read()), original_length + 1)

    def test_filter(self):
        self.inventoryDB.add(name="testInventory")
        self.assertIsNotNone(self.inventoryDB.filter(
            name="testself.inventory"))

    def test_edit(self):
        self.inventoryDB.add(name="testInventory")
        self.inventoryDB.update(
            {"name": "testInventory"},
            {"name": "testUpdate"}
        )
        self.assertIsNotNone(self.inventoryDB.filter(name="testInventory"))

    def test_delete(self):
        result = self.inventoryDB.read()
        delete_this, original_length = result[0], len(result)
        self.inventoryDB.delete(id=delete_this.id)
        self.assertEqual(len(self.inventoryDB.read()), original_length - 1)

    def test_flush(self):
        self.inventoryDB.flush_all()
        self.assertEqual(self.inventoryDB.read(), [])

    
