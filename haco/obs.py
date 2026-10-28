"""

Observability and logging setup for the haco library.

"""
from corio import logs, debug, Constants

from haco.paths import paths

debug.trace()

logger = logs.get_logger(
    name=paths.name,
    stream=Constants.DEVELOPMENT,
    version=paths.metadata.version,
)
