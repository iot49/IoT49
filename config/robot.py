# robot.py

Package(
    name = 'stm32-boot',
    src = [ 'boards/stm32/code/boot' ]
)

Package(
    name = 'stm32',
    src = [ 'boards/stm32/code/base', 'projects/robot/code-stm32' ],
    dst = 'lib',
    requires = 'secrets',
)

Package(
    name = 'esp32-robot',
    src = [ 'projects/robot/code-esp32' ],
)

#############################################################
# robot controller (stm32)

DeviceConfig(
    name = 'robot-stm',
    uid = '2d:00:49:00:09:50:52:42:4e:30:39:20',
    dest = '/spi',
    packages = [ ('stm32-boot', '/flash'), 
                  'stm32', 'bno055', 'vl53l0x', 'vl53l1x', 'pystone' ],
)

DeviceConfig(
    name = 'stm32',
    uid = '2c:00:29:00:09:50:52:42:4e:30:39:20',
    dest = '/spi',
    packages = [ ('stm32-boot', '/flash'),
                  'stm32', 'bno055', 'vl53l0x', 'vl53l1x', 'pystone' ],
)


#############################################################
# robot remote (esp32)

DeviceConfig(
    name = 'robot-remote',
    uid = '30:ae:a4:28:39:f0',
    packages = [ 'esp32-robot' ],
)

DeviceConfig(
    name = 'robot-remote-old',
    uid = '30:ae:a4:1a:2a:10',
    packages = [ 'esp32-robot' ],
)
