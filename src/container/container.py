import contextvars

from contextlib import contextmanager


class Container:

    @contextmanager
    def __call__(self):
        yield self._context.get()

    def __init__(self):
        self._context = contextvars.ContextVar("ctx", default={})

    def set(self, key, value):
        # if first time set is called, it is returning an empty dict for us to set the value into
        store = self._context.get().copy()
        store[key] = value
        self._context.set(store)

    def get(self, key):
        store = self._context.get(dict())
        return store.get(key)

    def remove(self, key):
        store = self._context.get().copy()
        if key in store:
            store.pop(key)
        self._context.set(store)


container = Container()
