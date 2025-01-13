from src.resources.key_store.key_store_interface import KeyStoreInterface


class InMemoryKeyStore (KeyStoreInterface):

    def __init__(self):
        self.data = dict()

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)
