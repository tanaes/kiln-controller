import board
from adafruit_dotstar import DotStar
from adafruit_led_animation.helper import PixelSubset
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.pulse import Pulse
import adafruit_led_animation.color as color



class dotstar(object):
    def __init__(self,
                 clk_pin,
                 dat_pin,
                 n,
                 groups=None):

        self.pins = {10: board.D10,
                     11: board.D11,
                     12: board.D12,
                     13: board.D13,
                     14: board.D14,
                     15: board.D15,
                     16: board.D16,
                     17: board.D17,
                     18: board.D18,
                     19: board.D19,
                     2:  board.D2,
                     20: board.D20,
                     21: board.D21,
                     22: board.D22,
                     23: board.D23,
                     24: board.D24,
                     25: board.D25,
                     26: board.D26,
                     27: board.D27,
                     3:  board.D3,
                     4:  board.D4,
                     5:  board.D5,
                     6:  board.D6,
                     7:  board.D7,
                     8:  board.D8,
                     9:  board.D9}

        self.clk_pin = self.pins[clk_pin]
        self.dat_pin = self.pins[dat_pin]
        self.n = n

        self.dots = DotStar(self.clk_pin,
                            self.dat_pin,
                            self.n,
                            brightness=0.2)

        if groups:
            if groups['time']['start'] > groups['time']['end']:
                self.time_reverse = True
                self.time_dots = PixelSubset(self.dots,
                                        groups['time']['end'],
                                        groups['time']['start'])
            else:
                self.time_reverse = False
                self.time_dots = PixelSubset(self.dots,
                                        groups['time']['start'],
                                        groups['time']['end'])

            if groups['temp']['start'] > groups['temp']['end']:
                self.temp_reverse = True
                self.temp_dots = PixelSubset(self.dots,
                                        groups['temp']['end'],
                                        groups['temp']['start'])
            else:
                self.temp_reverse = False
                self.temp_dots = PixelSubset(self.dots,
                                        groups['temp']['start'],
                                        groups['temp']['end'])

            if groups['status']['start'] > groups['status']['end']:
                self.status_reverse = True
                self.status_dots = PixelSubset(self.dots,
                                        groups['status']['end'],
                                        groups['status']['start'])
            else:
                self.status_reverse = False
                self.status_dots = PixelSubset(self.dots,
                                        groups['status']['start'],
                                        groups['status']['end'])
        else:
            self.time_dots = None
            self.temp_dots = None
            self.status_dots = None

    def time(self, totaltime, runtime):
        if self.time_dots is None:
            return()

        n_dots = self.time_dots.n

        inc = totaltime/n_dots

        if self.time_reverse:
            set1 = (n_dots - int(runtime/inc), n_dots)
            set2 = (0, n_dots - int(runtime/inc) - 1)
        else:
            set1 = (0, int(runtime/inc))
            set2 = (int(runtime/inc) +1, n_dots)

        past_dots = PixelSubset(self.time_dots,
                                  set1[0],
                                  set1[1])
        
        future_dots = PixelSubset(self.time_dots,
                                  set2[0],
                                  set2[1])
                                
        animations = AnimationSequence(
                        AnimationGroup(
                            Pulse(past_dots, 0.1, color.CYAN),
                            Pulse(future_dots, 0.1, color.WHITE),
                            sync=True))

        animations.animate()

    def temp(self, temperature, target):
        if self.temp_dots is None:
            return()

        n_dots = self.temp_dots.n

        inc = target/n_dots

        if self.temp_reverse:
            set1 = (n_dots - int(temperature/inc), n_dots)
            set2 = (0, n_dots - int(temperature/inc) - 1)
        else:
            set1 = (0, int(temperature/inc))
            set2 = (int(temperature/inc) +1, n_dots)

        past_dots = PixelSubset(self.temp_dots,
                                  set1[0],
                                  set1[1])
        
        future_dots = PixelSubset(self.temp_dots,
                                  set2[0],
                                  set2[1])
                                
        animations = AnimationSequence(
                        AnimationGroup(
                            Pulse(past_dots, 0.1, color.RED),
                            Pulse(future_dots, 0.1, color.WHITE),
                            sync=True))

        animations.animate()

    def idle(self):
        animation = Pulse(self.dots, 0.1, color.WHITE)

        animation.animate()