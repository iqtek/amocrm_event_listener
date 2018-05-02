import sys, os
sys.path.append( os.path.abspath(__file__) )

import lib.logutils as logutils
import lib.utils as utils
import lib.export as export
from settings import SETTINGS
import traceback

from lib.ami import Ami as Ami
from time import sleep

logger = logutils.get_pretty_logger(__name__)

def subscribe(ami, worker):
    """For loaded Moduler Event subscribe"""

    if hasattr(worker, "event"):
        for event in worker.event:
            if isinstance(event, (str, unicode)):
                functionName = "handle_" + event
                if hasattr(worker, functionName):
                    functionToCall = getattr(worker, functionName)
                    ami.events.subscribe(event, functionToCall)
    return

def main():
    """main loop"""

    plugins = export.load_modules()

    logger.info('Listener has been started')
    timeout = utils.increase_timeout_fibonacci()

    while True:
        try:
            ami = Ami.getInstance()
            for plugin in plugins.values():
                subscribe(ami, plugin)
            timeout = utils.increase_timeout_fibonacci()
            break
        except Exception as err:
            Ami.reconnect()

            logger.error(format(err))
            logger.debug(traceback.format_exc())

            time = timeout.next()
            logger.error('sleep: '+str(time))

            sleep(time)

    while True:
        try:
            #import ipdb; ipdb.set_trace()
            ami.serve_forever()
            timeout = utils.increase_timeout_fibonacci()
        except Exception as err:
            Ami.reconnect()

            logger.error(format(err))
            logger.debug(traceback.format_exc())

            time = timeout.next()
            logger.error('sleep: '+str(time))
            sleep(time)

if __name__ == '__main__':
    pid = str(os.getpid())
    if os.path.isfile(SETTINGS["PIDFILE"]):
        print "%s already exists, exiting" % SETTINGS["PIDFILE"]
        sys.exit()
    file(SETTINGS["PIDFILE"], 'w').write(pid)
    try:
        main()
    finally:
        os.unlink(SETTINGS["PIDFILE"])
