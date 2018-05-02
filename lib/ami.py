#import sys
#import os
from settings import AMI_SETTINGS as SETTINGS
#sys.path.append(os.path.join(os.path.dirname(__file__), '../', ''))

from Asterisk.Manager import Manager

__all__ = ["Ami", ]


class Ami(object):
    instance = None

    def getConnectin(self):
        return Manager(
            (SETTINGS["host"], SETTINGS["port"]),
            SETTINGS["login"],
            SETTINGS["password"],
            listen_events=True
        )

    def getInstance(self):
        if self.instance is None:
            self.instance = self.getConnectin()
        return self.instance

    def reconnect(self):
        if not self.instance is None:
            self.instance._connect()
        # del self.instance
        # return self.getInstance()

Ami = Ami()