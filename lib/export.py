import lib.logutils as logutils
import traceback

from settings import SETTINGS as SETTINGS
from importlib import import_module

logger = logutils.get_pretty_logger(__name__)


def load_modules():
    prefix = "modules"
    modules = {}
    
    for module in SETTINGS["MODULES"]:
        try:
            m = import_module("{}.{}".format(prefix, module))
            #if hasattr(m.worker, "BASE") and m.worker.BASE is None:
            #    m.worker.BASE = BASE
            modules[module] = m.worker
        except ImportError:
            logger.debug(traceback.format_exc())
            logger.error("Can not import module {}!".format(module))
    return modules
