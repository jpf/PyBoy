#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

from libc.stdint cimport uint8_t, uint16_t, uint32_t, uint64_t

import cython
cimport pyboy.core.cpu
cimport pyboy.core.timer
cimport pyboy.core.cartridge.base_mbc
from pyboy.utils cimport IntIOInterface
cimport pyboy.core.bootrom
cimport pyboy.core.ram
cimport pyboy.core.lcd
cimport pyboy.core.interaction
cimport pyboy.core.sound
from pyboy.utils cimport WindowEvent

cdef uint16_t STAT, LY, LYC
cdef short VBLANK, LCDC, TIMER, SERIAL, HIGHTOLOW

cdef class Motherboard:
    cdef pyboy.core.interaction.Interaction interaction
    cdef pyboy.core.bootrom.BootROM bootrom
    cdef pyboy.core.ram.RAM ram
    cdef pyboy.core.lcd.LCD lcd
    cdef pyboy.core.cpu.CPU cpu
    cdef pyboy.core.timer.Timer timer
    cdef bint sound_enabled
    cdef pyboy.core.sound.Sound sound
    cdef pyboy.core.cartridge.base_mbc.BaseMBC cartridge
    cdef bint bootrom_enabled
    cdef str serialbuffer

    cdef bint breakpoints_enabled
    cdef list breakpoints_list
    cdef int breakpoint_latch

    cdef void buttonevent(self, WindowEvent)
    cdef void stop(self, bint)
    @cython.locals(cycles=cython.int)
    cdef bint tick(self)

    cdef uint8_t getitem(self, uint16_t)
    cdef void setitem(self, uint16_t, uint8_t)

    @cython.locals(offset=cython.int, dst=cython.int, n=cython.int)
    cdef void transfer_DMA(self, uint8_t)
    cdef void save_state(self, IntIOInterface)
    cdef void load_state(self, IntIOInterface)

    cdef long ticks
    cdef object logfile