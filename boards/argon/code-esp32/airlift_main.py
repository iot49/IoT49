import uasyncio as asyncio
import urpc_server
import machine

BAUDRATE = 1_000_000

# maximum number of bytes returned by socket.readinto
READINTO_BUFFER_SIZE = 512

# WDT timeout [ms]
# Note: longest exec (urpc, mp) << WDT_TIMEOUT
WDT_TIMEOUT = 120000

# for Particle Argon
uart_config = { 'rx': 19, 'tx': 22, 'rts': 0, 'cts': 26, 
                'rxbuf': 2048, 'txbuf': 1024,
                'baudrate': BAUDRATE }

uart = machine.UART(2, **uart_config)
uart.init(bits=8, stop=2, parity=None, timeout=300)

async def wdt_feeder():
    wdt = machine.WDT(timeout=WDT_TIMEOUT)
    while True:
        await asyncio.sleep_ms(WDT_TIMEOUT // 3)
        wdt.feed()

async def main():
    asyncio.create_task(wdt_feeder())
    asyncio.create_task(urpc_server.async_serve(uart, READINTO_BUFFER_SIZE))
    asyncio.get_event_loop().run_forever()
    
asyncio.run(main())
