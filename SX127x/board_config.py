""" Defines the BOARD class that contains the board pin mappings. """

# Copyright 2015 Mayer Analytics Ltd.
#
# This file is part of pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.


from machine import Pin,SPI

import time


class BOARD:
    """ Board initialisation/teardown and pin configuration is kept here.
        This is the Raspberry Pi board with one LED and a modtronix inAir9B
    """
    # Note that the BCOM numbering for the GPIOs is used.
    P_DIO0 = 5
    P_DIO1 = 4
    #P_DIO2 = 24
    #P_DIO3 = 25
    P_LED  = 2
    P_SWITCH = 0

    # The spi object is kept here
    spi = None

    @staticmethod
    def setup():
        # LED
        BOARD.LED = Pin(BOARD.P_LED, Pin.OUT, value=0)
        # switch
        BOARD.SWITCH = Pin(BOARD.P_SWITCH, Pin.IN, Pin.PULL_UP) 
        # DIOx
        BOARD.DIO0 = Pin(BOARD.P_DIO0, Pin.IN)
        BOARD.DIO1 = Pin(BOARD.P_DIO1, Pin.IN)
        # blink 2 times to signal the board is set up
        BOARD.blink(.1, 2)

    @staticmethod
    def teardown():
        """ Cleanup GPIO and SpiDev """
        BOARD.spi.deinit()

    @staticmethod
    def SpiDev(spi_bus=0, spi_cs=0):
        """ Init and return the SpiDev object
        :return: SpiDev object
        :param spi_bus: The RPi SPI bus to use: 0 or 1
        :param spi_cs: The RPi SPI chip select to use: 0 or 1
        :rtype: SpiDev
        """
        return BOARD.spi(1,baudrate=1000000)

    @staticmethod
    def add_event_detect(dio_number, callback):
        """ Wraps around the GPIO.add_event_detect function
        :param dio_number: DIO pin 0...5
        :param callback: The function to call when the DIO triggers an IRQ.
        :return: None
        """
        dio_number.irq(trigger=Pin.IRQ_RISING, handler=callback)

    @staticmethod
    def add_events(cb_dio0, cb_dio1, switch_cb=None):
        BOARD.add_event_detect(BOARD.DIO0, cb_dio0)
        BOARD.add_event_detect(BOARD.DIO1, cb_dio1)

        # the modtronix inAir9B does not expose DIO4 and DIO5
        if switch_cb is not None:
            BOARD.add_event_detect(BOARD.SWITCH, switch_cb)

    @staticmethod
    def blink(time_sec, n_blink):
        if n_blink == 0:
            return
        BOARD.LED.on()
        for i in range(n_blink):
            time.sleep(time_sec)
            BOARD.LED.off()
            time.sleep(time_sec)
            BOARD.LED.on()
        BOARD.LED.off()
