#!/usr/bin/env python3

import sys

from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import (
    characteristic,
    CharacteristicFlags as CharFlags,
)
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags
from bluez_peripheral.gatt.service import ServiceCollection
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
import asyncio

import os
import subprocess

LIGHT_STRIP_SERVICE_ID = "55F35C03-6E4B-436B-9231-11A9D3EB2D0C"

# Define a service like so.
class LightStripService(Service, ):
    def __init__(self):
        # Advertise the service for 3600 seconds, then do it again
        self.TIMEOUT=3590
        self.SLEEP_TIME=5
        self.agent = NoIoAgent()
        # Call the super constructor to set the UUID.
        super().__init__(LIGHT_STRIP_SERVICE_ID, True)

    async def run(self):
        bus = await get_message_bus()

        while True:
            # Instance and register your service.
            await self.register(bus)
            # This script needs superuser for this to work.
            await self.agent.register(bus)
            adapter = await Adapter.get_first(bus)
            advert = Advertisement("Lamp Test", [LIGHT_STRIP_SERVICE_ID], 0x04C3, self.TIMEOUT)
            await advert.register(bus, adapter)
            sleeps = 0
            while sleeps < self.TIMEOUT//self.SLEEP_TIME:
                await asyncio.sleep(self.SLEEP_TIME)
                sleeps += 1
            await self.unregister()
            await asyncio.sleep(self.SLEEP_TIME)




if __name__ == "__main__":
    asyncio.run(start())
