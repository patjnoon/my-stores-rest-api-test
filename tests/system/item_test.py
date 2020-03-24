import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest

class ItemTest(BaseTest):
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                request = client.get('/item/test-item')
                self.assertEqual(request.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                UserModel('patn', '1234').save_to_db()
                auth_request = client.post('/auth', data=json.dumps({'username':'patn', 'password':'1234'}),
                                           headers={'Content-Type':'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                header = {'Authorization':'JWT ' + auth_token}
                request = client.get('/item/test-item', headers=header)
                self.assertEqual(request.status_code, 404)
