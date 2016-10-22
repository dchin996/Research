'''
This script sends a square wave signal
It sends a (1) by flashing the fingerprint sensor on
and sends a (0) by leaving the sensor off
It uses uint8 data type and converts it to binary to send a signal
It uses fprint_codes.py to send these signals as well as the BSAPI c library
'''

from ctypes import *
from ctypes.util import find_library
from time import sleep
import argparse
import time

import numpy as np
from fprint_codes import check_call, callback_message

delay="""
delay | ms  \n
============\n
1     | 40,
100   | 171,
250   | 276,
460   | 480,
500   | 586,
1000  | 1.081,
"""

class ABS_IMAGE_FORMAT(Structure):
    _fields_ = [("scan_resolution_h", c_ushort),
                ("scan_resolution_v", c_ushort),
                ("image_resolution_h", c_ushort),
                ("image_resolution_v", c_ushort),
                ("scan_bits_per_pixel", c_ubyte),
                ("image_bits_per_pixel", c_ubyte)]

class ABS_IMAGE(Structure):
    """
    Holds data representing one sample image of swiped finger.

    """
    _fields_ = [("width", c_uint),
                ("height", c_uint),
                ("color_count", c_uint),
                ("horizontal_dpi", c_uint),
                ("vertical_dpi", c_uint),
                ("image_data", POINTER(c_ubyte))]

# forward declaration
class ABS_OPERATION(Structure):
    pass

CALLBACKFUNC = CFUNCTYPE(c_uint, POINTER(ABS_OPERATION),
                         c_uint, c_void_p)

# complete definition of ABS_OPERATION
ABS_OPERATION._fields_ = [("operation_id", c_uint),
                          ("context", c_void_p),
                          ("callback", CALLBACKFUNC),
                          ("timeout", c_int),
                          ("flags", c_uint)]

def bsapi_callback(operation_param, message, data):
    try:
      msg = callback_message(message)
      if msg: print(msg)
    except:
      print('error')
    return message

class FMDevice:
    """
    Connection to a Fingerprint Module (FM) using the UPEK Biometric
    Services API

    """
    def __init__(self, t):
        self.timeout = t

        # load libbsapi.so; must be located in /usr/lib or /usr/lib64
        self.__bsapi = CDLL(find_library("bsapi"))

        # initialize the bsapi subsystem
        check_call(self.__bsapi.ABSInitialize())

        # open a connection to a usb device
        self.__conn_handle = c_int(0)
        # use a byte string to produce a c_char_p instead of a
        # c_wchar_p
        check_call(self.__bsapi.ABSOpen(b"usb",
                                        byref(self.__conn_handle)))
        self.image_format = self.__get_image_format()


    def __get_image_format(self):
        num_formats = c_uint()
        format_list = POINTER(ABS_IMAGE_FORMAT)() # null pointer

        check_call(self.__bsapi.ABSListImageFormats(
            self.__conn_handle, byref(num_formats),
            byref(format_list), c_uint(0)))

        if not num_formats.value:
            print("No appropiate image formats found")
            return None
        else:
            # use the first format in the returned list
            image_format = ABS_IMAGE_FORMAT()
            pointer(image_format)[0] = format_list[0] # necessary for
                                                      # a deep copy?
            self.__bsapi.ABSFree(format_list)
            return image_format

    def grab_image(self):
        image_format = self.__get_image_format()
        if not image_format:
            return

       #try:
       #  print("before")
        operation_parameters = ABS_OPERATION(
            0, # operation ID; doesn't matter
            None, # data to pass to callback
            CALLBACKFUNC(bsapi_callback),
            1, # timeout
            0x1) # callback flag (nowait)
       #  sleep(1)
       #  return
       #except:
       #  print("error")

        image = POINTER(ABS_IMAGE)()

        check_call(self.__bsapi.ABSGrabImage(self.__conn_handle,
            byref(operation_parameters), 0, # ABS_PURPOSE_UNDEFINED
            byref(image_format), byref(image), # what we want!
            None, # swipe info, if desired
            None, # reserved
            0)) # flags

       ## copy image to Python format
       #print("Recieved image.", "{}x{} pixels, {} colors".format(
       #    image.contents.width, image.contents.height,
       #    image.contents.color_count))

       #data = []
       #print(image.contents.image_data)
       ##for i in range(image.contents.width * image.contents.height):
       ##    data.append( int(image.contents.image_data[i]) )
       #print("Datalen:", len(data))

       ##self.__bsapi.ABSFree(image)

       #return image

    def test(self):

        operation_parameters = ABS_OPERATION(
            0, # operation ID; doesn't matter
            None, # data to pass to callback
            CALLBACKFUNC(bsapi_callback),
            self.timeout, # timeout
            0x1) # callback flag (nowait)

        image = POINTER(ABS_IMAGE)()

        check_call(self.__bsapi.ABSGrabImage(self.__conn_handle,
            byref(operation_parameters), 0, # ABS_PURPOSE_UNDEFINED
            byref(self.image_format), byref(image), # what we want!
            None, # swipe info, if desired
            None, # reserved
            0)) # flags

    def __del__(self):
        if self.__conn_handle.value:
            # close connection
            self.__bsapi.ABSClose(self.__conn_handle)

        # close out the bsapi subsystem
        self.__bsapi.ABSTerminate()


def main():
  preamble_data = [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1] # 13 bit barker code, 
  #preamble_data = [1, 1, 1, 1, 1]
  # if you want to change, make sure it is an uint8
  preamble = np.array(preamble_data, dtype="uint8") # 31, 53 is standard
  fm = FMDevice(50)
  print("Sending preamble")
  binary_code = preamble
  # binary_code = uint8_to_binary(preamble) # only needed if preamble_data needs to be converted from byte to bit
  send_code(string=binary_code, fm=fm)
  print("preamble done")
  send_payload(fm)
  time.sleep(.250)
  for i in range(99):
    send_code(string=binary_code, fm=fm)
    send_payload(fm)
    time.sleep(.250)

  # send_code(string="01001010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101", fm=fm)


def uint8_to_binary(uint8):
  binary_code = ""
  for x in range(uint8.size):
    bin_val = bin(uint8[x])
    for y in range(8 - (len(bin_val) - 2)):
      binary_code += "0"
    for y in range(len(bin_val) - 2):
      binary_code += bin_val[y + 2]
  return binary_code

def send_code(string, fm):
  for i in range(len(string)):
    if (string[i] == "1") or (string[i] == 1):
      #t1 = time.time()
      try:
        fm.test()
      except KeyboardInterrupt:
        del fm
        quit()
      except:
        pass
        print("1")
      #t2 = time.time()
      #print("1 time = " + str(t2 - t1))
    else:
      #t1 = time.time()
      time.sleep(177/1000.0)
      #t2 = time.time()
      #print("0 time = " + str(t2 - t1))
      print("0")
    
def send_payload(fm):
  payload_data = [170] #170 converts to "10101010"
  payload = np.array(payload_data, dtype="uint8")
  send_code(uint8_to_binary(payload), fm)



if __name__ == '__main__':
	main()
