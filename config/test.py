# test.py

#############################################################
# argon
DeviceConfig(
    name = 'test-argon',
    uid = '65:45:95:1c:95:25:2a:25',
    packages = ['secrets',
                'uasyncio',
                'airlift-client',
                'mp-server',
                ('boards/argon/code-esp32', '/esp32'),
                'boards/argon/code' ])

DeviceConfig(
    uid = '30:ae:a4:d1:7c:40',
    name = 'test-argon-cop',
    packages = [ 'secrets', 'boards/argon/code-esp32' ])


#############################################################
# esp32
DeviceConfig(
    uid = '30:ae:a4:30:84:34',
    name = 'test-esp32',
    packages = [ 'secrets', 'mp-server', 'esp32' ])


#############################################################
# stm32
DeviceConfig(
    uid = '27:00:55:00:09:50:52:42:4e:30:39:20',
    name = 'test-stm32',
    packages = [
        ('boards/stm32/code/boot', '/flash'),
        'secrets', 'airlift-client', 'mp-server',
        'boards/stm32/code/base' ],
    dest = '/spi')

DeviceConfig(
    uid = '30:ae:a4:1a:2c:3c',
    name = 'test-stm32-cop',
    packages = [ 'secrets', 'airlift-server', 'mp-server', 'boards/stm32/code-esp32' ])


#############################################################
# samd51
DeviceConfig(
    uid = '28:eb:07:5a:32:43:37:53:20:20:20:31:05:20:0f:ff',
    name = 'test-samd',
    packages = [
        'secrets',
        'mp-server',
        'airlift-client',
        ('airlift-server', '/esp32'),
        'boards/samd51/code' ] )
