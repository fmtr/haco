import asyncio
import logging

from haco.button import Button
from haco.client import ClientHaco
from haco.climate import Climate
from haco.constants import MQTT_HOST
from haco.device import Device
from haco.obs import logger
from haco.select import Select
from haco.switch import Switch

handler = logger.LogfireLoggingHandler()
logging.basicConfig(handlers=[handler], level=logging.DEBUG)

async def main():
    climate_a = Climate(name="Dev Climate A", fan_modes=['a', 'b', 'c'])
    climate_b = Climate(name="Dev Climate B", fan_modes=['a', 'b', 'c'])

    b1 = Button(name="Dev Button 1")

    s1 = Switch(name="Dev Switch 1")
    sel1 = Select(name="Dev Select 1", options=['a', 'b', 'c'])
    device = Device(name="Dev Device", controls=[climate_a, climate_b, b1, s1, sel1])

    client = ClientHaco(hostname=MQTT_HOST, device=device, logger=logging.getLogger(__name__))

    await client.start()




if __name__ == "__main__":
    asyncio.run(main())
