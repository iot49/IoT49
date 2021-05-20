# argon.py

Package("argon", "boards/argon/code", requires="secrets")


#############################################################
# robot-argon

DeviceConfig(
    name = 'robot-argon',
    uid = 'cf:ec:09:07:44:72:94:6f',
    packages = ['argon'])
