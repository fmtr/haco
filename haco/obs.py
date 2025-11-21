from fmtr.tools import logging, debug, Constants
from haco.paths import paths
from haco.version import __version__

debug.trace()

logger = logging.get_logger(
    name=paths.name_ns,
    stream=Constants.INFRA,
    version=__version__,
)
