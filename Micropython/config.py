# Copyright 2020 LeMaRiva|tech lemariva.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

MSG_TIMEOUT = 60 #Timeout in seconds

"""
# ES32 TTGO v1.0 
device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':14,
    'led':2, 
}
# M5Stack ATOM Matrix
device_config = {
    'miso':23,
    'mosi':19,
    'ss':22,
    'sck':33,
    'dio_0':25,
    'reset':21,
    'led':12, 
}
"""

 # Lilygo T3 v1.6.1   
# device_config = {
    # 'miso':19,
    # 'mosi':27,
    # 'ss':18,
    # 'sck':5,
    # 'dio-0':26,
    # 'reset':23,
    # 'led':25,
# }


# ~ # wroom with external radio
device_config= {
    'miso':19,
    'mosi':23,
    'ss':5,
    'sck':18,
    'dio_0':25,
    'reset':26,
    'led':33, 
}

# wroom with battery and external radio (vape battery)
# device_config= {
    # 'miso':19,
    # 'mosi':23,
    # 'ss':5,
    # 'sck':18,
    # 'dio_0':17,
    # 'reset':16,
    # 'led':13, 
# }

# wroom with battery and external radio
# device_config= {
    # 'miso':23,
    # 'mosi':19,
    # 'ss':5,
    # 'sck':18,
    # 'dio_0':17,
    # 'reset':16,
    # 'led':13, 
# }

'''
# heltec_lora
device_config= {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':14,
    'led':25, 
}
'''

app_config = {
    'loop': 200,
    'sleep': 100,
}

lora_parameters = {
    'frequency': 915E6, 
    'tx_power_level': 17, 
    'signal_bandwidth': 70E3,    
    'spreading_factor': 12, 
    'coding_rate': 1, 
    'preamble_length': 8,
    'implicit_header': False, 
    'sync_word': 0x12, 
    'enable_CRC': False,
    'invert_IQ': False,
}

wifi_config = {
    'ssid':'',
    'password':''
}


#esp32 no battery prototype
relay_pins = {'flasher_pin':14,
              'hv_pin':27,
              'batt1_pin':33,
              'batt2_pin':32,
    }   


relay_names = {14:"flasher_pin",
               27:"hv_pin",
               33:"batt1_pin",
               32:"batt2_pin",
        }

fadcratios = {
'solrat': 4.25E-3, #volts/fadc
'solpin': 35,
'batt1rat': 4.28E-3,
'batt1pin':34,
# 'batt2rat': 4.25E-3,
# 'batt2pin':0,
}



#esp32 with battery prototype
'''
relay_pins = {'flasher_pin':12,
              'solar_pin':14,
              'batt1_pin':27,
              'batt2_pin':26,
    }   

relay_names = {12:"flasher_pin",
               14:"solar_pin",
               27:"batt1_pin",
               26:"batt2_pin",
        }

fadcratios = {
'solrat': 4.25E-3, #volts/fadc
'solpin': 32,
'batt1rat': 4.25E-3,
'batt1pin':33,
'batt2rat': 4.25E-3,
'batt2pin':34,
}
'''
