import memcache
from settings import MEMCACHE as SETTINGS

__all__ = ["Memcached", ]


class Memcache(object):
    instance = None

    def getConnectin(self):
        return memcache.Client(
            [SETTINGS["HOST"] +':' + SETTINGS["PORT"]],
            #pickler=SimplejsonWrapper,
            #unpickler=SimplejsonWrapper
        )

    def getInstance(self):
        if self.instance is None:
            self.instance = self.getConnectin()
        return self.instance

    def reconnect(self):
        del self.instance
        return self.getInstance()

Memcached = Memcache()