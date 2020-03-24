from models.store import StoreModel
from models.item import ItemModel

from tests.base_test import BaseTest

class StoreTest(BaseTest):

    def test_create_store_items_empty(self):

        store = StoreModel("test-store")
        self.assertListEqual(store.items.all(), [ ])


    def test_crud(self):

        with self.app_context():
            store = StoreModel("test-store")
            self.assertIsNone(StoreModel.find_by_name('test-store'))

            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('test-store'))

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('test-store'))

    def test_store_json_no_item(self):

        with self.app_context():

            store = StoreModel("test-store")
            store.save_to_db()

            expected = {
                'name': 'test-store',
                'items': []
            }

            self.assertDictEqual(store.json(), expected)


    def test_store_json_one_item(self):

        with self.app_context():

            store = StoreModel("test-store")
            store.save_to_db()

            ItemModel("test-item", 19.99, 1).save_to_db()

            expected = {
                'name': 'test-store',
                'items': [{'name': 'test-item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected)
