import unittest
from project import app


class InventoryServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flaskr.app.test_client()

    def test_mainPage(self):
        result = self.app.get('/', content_type='html/text')
        self.assertEqual(result.status_code, 200)

    def test_new_category(self):
        tester = app.test_client(self)
        result = tester.get(
            '/inventory/1/category/new',
            content_type='html/text')
        self.assertEqual(result.status_code, 200)
    
    def test_edit_category(self):
        tester = app.test_client(self)
        result = tester.get(
            '/inventory/1/category/1/edit',
            content_type='html/text')
        self.assertEqual(result.status_code, 200)
    
    def test_delete_category(self):
        tester = app.test_client(self)
        result = tester.get(
            '/inventory/1/category/1/delete',
            content_type='html/text'
        )
        self.assertEqual(result.status_code, 200)
    
    def test_show_item_details(self):
        tester = app.test_client(self)
        result = tester.get(
            '/inventory/<int:inventory_id>\
                /category/<int:category_id>/item/<int:item_id>/',
            content_type='html/text')
        self.assertEqual(result.status_code, 200)
    
    def test_new_item(self):
        tester = app.test_client(self)
        result = tester.get(
            '/inventory/<int:inventory_id>\
                /category/<int:category_id>/item/new',
            content_type='html/text')
        self.assertEqual(result.status_code, 200)
    
    def test_edit_item(self):
        tester = app.test_client(self)
        result = tester.get(
            '/inventory/<int:inventory_id>\
                /category/<int:category_id>/item/<int:item_id>/edit',
            content_type='html/text')
        self.assertEqual(result.status_code, 200)
    
    def test_delete_item(self):
        tester = app.test_client(self)
        result = tester.get(
            '/inventory/<int:inventory_id>\
                /category/<int:category_id>/item/<int:item_id>/delete',
            content_type='html/text')
        self.assertEqual(result.status_code, 200)
    
    def test_main_page(self):
        tester = app.test_client(self)
        result = tester.get('/', content_type='html/text')
        self.assertEqual(result.status_code, 200)
    
    
if __name__ == '__main__':
    unittest.main()        
        