#!/usr/bin/env python3

import sys

sys.path.append('/root/workspace')

from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import (
    characteristic,
    CharacteristicFlags as CharFlags,
)
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags
from bluez_peripheral.gatt.service import ServiceCollection
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
from agent import MyAgent
import asyncio

import os
import subprocess

LAMP_STATUS_EXEC = "/root/workspace/lampAdjustment"
LAMP_ON = 1
LAMP_OFF = 0

# Define a service like so.
class LampService(Service):
    def __init__(self):
        self.lamp_status = LAMP_OFF
        # Call the super constructor to set the UUID.
        super().__init__("ABC0", True)

    @characteristic("ABC1", CharFlags.READ)
    def health_check(self, options):
        # Characteristics need to return bytes.
        return bytes("Hello World!", "utf-8")
    
    def change_lamp_status(self, value):
        proc = subprocess.run([LAMP_STATUS_EXEC, f"{value}"])
        print("Finished running the subprocess: ")
        print(proc)

    @characteristic("ABC2", CharFlags.WRITE_WITHOUT_RESPONSE)
    def update_lamp_status(self, options):
        print("Inside the garbage write function")
        pass

    # This is a write only characteristic.
    @update_lamp_status.setter
    def update_lamp_status(self, value, options):
        print("Inside the actual setter function")
        print(value)
        if self.lamp_status == LAMP_ON:
            self.lamp_status = LAMP_OFF
        else:
            self.lamp_status = LAMP_ON
        self.change_lamp_status(self.lamp_status)

# Advertise the service for 3600 seconds, then do it again
TIMEOUT=3590
SLEEP_TIME=5

async def start():
    # This needs running in an awaitable context.
    bus = await get_message_bus()



    while True:
        # Instance and register your service.
        service = LampService()
        await service.register(bus)

        # An agent is required to handle pairing
        agent = MyAgent()
        # This script needs superuser for this to work.
        await agent.register(bus)
        adapter = await Adapter.get_first(bus)
        advert = Advertisement("Lamp Test", ["ABC0"], 0x04C3, TIMEOUT)
        await advert.register(bus, adapter)
        sleeps = 0
        while sleeps < TIMEOUT//SLEEP_TIME:
            await asyncio.sleep(SLEEP_TIME)
            sleeps += 1
        await service.unregister()
        await asyncio.sleep(SLEEP_TIME)



    await bus.wait_for_disconnect()


if __name__ == "__main__":
    asyncio.run(start())
