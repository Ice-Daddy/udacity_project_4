"""
Test project.py
"""

import unittest
from project import app


class InventoryServerTestWithoutLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_main_page(self):
        result = self.app.get('/', content_type='html/text')
        self.assertEqual(result.status_code, 200)

    def test_show_inventory(self):
        result = self.app.get('/inventory/head/', content_type='html/text')
        self.assertEqual(result.status_code, 200)


class TestCRUDFunctionality(unittest.TestCase):

    def test_new_category(self):
        pass

    def test_edit_category(self):
        pass

    def test_delete_category(self):
        pass

    def test_new_item(self):
        pass

    def test_edit_item(self):
        pass

    def test_delete_item(self):
        pass


class TestAPI(unittest.TestCase):

    def test_list_inventory_types(self):
        pass

    def test_list_categories(self):
        pass

    def test_list_items_of_category(self):
        pass


if __name__ == '__main__':
    unittest.main()
