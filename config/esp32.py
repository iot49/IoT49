# esp32.py

Package("esp32", "boards/esp32/code/")

Package("ble32", "boards/esp32/libraries/bluetooth_examples", "lib")

#############################################################
# deepsleep current test

Package("power_test", "boards/esp32/libraries/power")

DeviceConfig(
    name = "power_test",
    uid = " 24:0a:c4:12:87:7c",
    packages = [ 'power_test' ]
)

#############################################################
# ble uart test

DeviceConfig(
    name = "ble_uart_test",
    uid = "24:0a:c4:12:87:7c",
    packages = [ 'esp32-robot' ],
)
