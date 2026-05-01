from corio import Setup

setup = Setup(
    org=None,
    dependencies=dict(
        install=[
            'corio[version.dev,logging,sets,yaml,debug,caching,api,mqtt]',
            'psutil'
        ],
        test=[
            'pytest>=8.0',
            'pytest-cov>=5.0',
        ],
    ),
    description='Home Assistant Control Objects',
    keywords='homeassistant controls python tasmota',
    # url=f'https://fmtr.link/{name}',
)
