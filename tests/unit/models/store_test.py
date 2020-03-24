from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel("test-store")

        self.assertEqual(store.name, "test-store", "The name of the store does not match constructor argument")
