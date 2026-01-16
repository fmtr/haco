from fmtr.tools import infra
from haco.paths import paths


class Project(infra.Project):
    """"""

    def __init__(self, entrypoint='launch', hostname='ws.lan', channel='dev', extras=None):
        super().__init__(

            # project
            base='python',
            name=paths.name,
            port=6,

            is_pypi=True,  # public release

            entrypoint=entrypoint,
            hostname=hostname,
            channel=channel,
            extras=extras
        )
