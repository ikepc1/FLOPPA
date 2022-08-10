import ssd1306
from machine import Pin,SoftI2C
import time

class Display:
    '''This class controls the lcd display on the heltec e32 lora v2'''
    oled_width = 128
    oled_height = 64
    # OLED reset pin
    i2c_rst = Pin(16, Pin.OUT)
    # Initialize the OLED display
    i2c_rst.value(0)
    time.sleep_ms(5)
    i2c_rst.value(1) # must be held high after initialization
    # Setup the I2C lines
    i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
    i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
    
    def __init__(self):
        self.i2c = SoftI2C(scl=self.i2c_scl, sda=self.i2c_sda)
        self.ssd1306 = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)
        self.ssd1306.fill(0)
        #self.display_text('Display started...')
        #time.sleep(2)
        #self.ssd1306.fill(0)
        
    def display_text(self, text, x=0, y=25):
        '''This method displays text on the screen
        parameters:
        text: the text to be displayed (str)
        x: x coordinate of the upper left corner of the text (int)
        y: y coordinate of the upper left corner of the text (int)
        '''
        self.ssd1306.fill(0)
        self.ssd1306.text(text, x, y)
        self.ssd1306.show()
        
    def display_lines(self, line_list):
        '''This method display
        '''
        if len(line_list) >= 8:
            self.display_text('Too many lines')
            print('Too many lines to display')
        else:
            self.ssd1306.fill(0)
            y_start = 0
            for line in line_list:
                self.ssd1306.text(line, 0, y_start)
                y_start += 9
            self.ssd1306.show()
            print('Lines printed')
        
# # Create the bus object
# i2c = SoftI2C(scl=i2c_scl, sda=i2c_sda)
# # Create the display object
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
# oled.fill(0)
# 
# oled.text('HELLO WiFi ESP32', 0, 25)
# oled.text('escapequotes.net', 0, 55)
#   
# #oled.line(0, 0, 50, 25, 1)
# oled.show()
