from fmtr.tools import Setup

setup = Setup(
    org=None,
    dependencies=dict(
        install=[
            'fmtr.tools[version.dev,logging,sets,yaml,debug,caching,api,mqtt]',
        ]
    ),
    description='Home Assistant Control Objects',
    keywords='homeassistant controls python tasmota',
    # url=f'https://fmtr.link/{name}',
)
