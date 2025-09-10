"""
Script from chat
"""

import asyncio
from bleak import BleakClient, BleakScanner

from wahoo.helper import handle_power_notification, POWER_UUID


async def main():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=5)
    print(devices, len(devices))
    # Try to find Wahoo device (you can also filter by MAC address or name)
    wahoo = None
    for device in devices:
        print(f"Found: {device.name} [{device.address}]")
        if "KICKR" in (device.name or ""):
            wahoo = device
            break
    
    if not wahoo:
        print("Wahoo device not found. Is it turned on and in range?")
        return

    print(f"Connecting to {wahoo.name} [{wahoo.address}]...")
    async with BleakClient(wahoo.address) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        print("Connected!")

        print("Subscribing to power notifications...")
        await client.start_notify(POWER_UUID, handle_power_notification)

        print("Streaming power... Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping...")

        await client.stop_notify(POWER_UUID)

asyncio.run(main())
