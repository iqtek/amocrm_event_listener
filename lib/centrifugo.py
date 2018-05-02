from cent.core import Client
from settings import CENTRIFUGO as SETTINGS

__all__ = ["Centrifugo", ]


class Centrifugo(object):
    instance = None

    def getConnectin(self):
        return Client(
            SETTINGS["URL"],
            SETTINGS["SECRET"]
        )

    def getInstance(self):
        if self.instance is None:
            self.instance = self.getConnectin()
        return self.instance

    def reconnect(self):
        del self.instance
        return self.getInstance()

Centrifugo = Centrifugo()