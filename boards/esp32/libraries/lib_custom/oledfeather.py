from ssd1306 import SSD1306_I2C
from writer import Writer
import freesans20
import board

A6 = const(14)
A7 = const(32)
A8 = const(15)

BUTTON_A = const(15)   # A8
BUTTON_B = const(32)   # A7
BUTTON_C = const(14)   # A6

class OledFeather:
    def __init__(self, i2c):
        self.ssd1306 = SSD1306_I2C(128, 64, i2c)
        self.writer = Writer(self.ssd1306, freesans20, verbose=False)
        self.writer.set_clip(True, True)

    def text(self, str, x=0, y=0):
        self.ssd1306.fill(0)
        self.writer.set_textpos(x, y)
        self.writer.printstring(str)
        self.ssd1306.show()

    def get_ssd(self):
        return self.ssd1306

    def get_writer(self):
        return self.writer()
