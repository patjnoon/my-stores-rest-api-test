from models.store import StoreModel
from tests.base_test import BaseTest
import json

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test-store')

                self.assertEqual(201, request.status_code)
                self.assertIsNotNone(StoreModel.find_by_name('test-store'))
                print(json.loads(request.data))
                self.assertDictEqual({'name': 'test-store', 'items': []}, json.loads(request.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test-store')
                request2 = client.post('/store/test-store')

                self.assertEqual(400, request2.status_code)
                print(json.loads(request2.data))

                self.assertDictEqual({'message': "A store with name 'test-store' already exists."}, json.loads(request2.data))

    def test_create_delete_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test-store')

                request2 = client.delete('/store/test-store')
                self.assertEqual(200, request2.status_code)
                self.assertDictEqual({'message': "Store deleted"}, json.loads(request2.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test-store')

                request2 = client.get('/store/test-store')
                self.assertEqual(200, request2.status_code)
                self.assertDictEqual({'name': 'test-store', 'items': []}, json.loads(request2.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test-store')

                request2 = client.get('/store/fake-store')
                self.assertEqual(404, request2.status_code)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(request2.data))


    def test_store_list(self):
        with self.app() as client:
            with self.app_context():

                request = client.post('/store/test-storeA')
                request2 = client.post('/store/test-storeB')
                request3 = client.get('/stores')
                self.assertEqual(200, request3.status_code)
                expected = {'stores': [
                    {'name': 'test-storeA', 'items': []},
                    {'name': 'test-storeB', 'items': []}
                    ]
                }
                self.assertDictEqual(expected, json.loads(request3.data))

    def test_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/store/test-store')

                request2 = client.post('/item/test-itemA', data={'name':'test-itemA', 'price': '19.99', 'store_id': '1'})
                print(request2.status_code)
                print(json.loads(request2.data))

                request3 = client.get('/stores')
                print(json.loads(request3.data))

                self.assertEqual(200, request3.status_code)
                expected = {'stores': [{'name': 'test-store', 'items': [{'name': 'test-itemA', 'price': 19.99}]}]}
                self.assertDictEqual(expected, json.loads(request3.data))
