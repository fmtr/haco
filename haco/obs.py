from corio import logging, debug, Constants
from haco.paths import paths


debug.trace()

logger = logging.get_logger(
    name=paths.name_ns,
    stream=Constants.INFRA,
    version=paths.metadata.version,
)
