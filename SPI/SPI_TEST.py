#!/usr/bin/python

"""
    Description: Teste do SPI0 via Raspberry pi
    Author: Bruno G. F. Sampaio 
    email: bruno.bielsam.1205@hotmail.com
    date: 17/01/2024
    version: 0.1.1
    Rev: 0.1
"""

import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100_000
spi.mode = 3

while 1:
  msg = [0xAB]
  res = spi.xfer2(msg)
  print("Result", res)
  time.sleep(1)