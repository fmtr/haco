import asyncio

from haco.client import ClientHaco
from haco.climate import Climate
from haco.constants import MQTT_HOST
from haco.device import Device


async def main():
    climate_a = Climate(name="Dev Climate A", fan_modes=['a', 'b', 'c'])
    climate_b = Climate(name="Dev Climate B", fan_modes=['a', 'b', 'c'])
    device = Device(name="Dev Device", controls=[climate_a, climate_b])

    client = ClientHaco(hostname=MQTT_HOST, device=device)

    await client.start()




if __name__ == "__main__":
    asyncio.run(main())
