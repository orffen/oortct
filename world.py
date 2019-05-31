# world.py -- Orffen's Referee Toolbox for Classic Traveller
# Copyright (c) 2019 Steve Simenic
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import csv
import random
from roll import roll
from uwp import UWP

class World(object):
    """
    Class for storing Traveller world information.

    If no arguments are passed, will generate a random world instead.

    Keyword arguments (all required if any passed):
    name          -- string
    starport      -- string containing starport type character
    contents      -- array of bool values (Naval Base, Scout Base, Gas Giant)
    size          -- integer
    atmosphere    -- integer
    hydrographics -- integer
    population    -- integer
    government    -- integer
    law_level     -- integer
    tech_level    -- integer

    """
    def __init__(self, name, starport, contents, size, atmosphere, 
                 hydrographics, population, government, law_level, tech_level):
        self.name          = name
        self.starport      = starport
        self.contents      = contents
        self.size          = size
        self.atmosphere    = atmosphere
        self.hydrographics = hydrographics
        self.population    = population
        self.government    = government
        self.law_level     = law_level
        self.tech_level    = tech_level
        self.uwp           = UWP(self.starport, self.size, self.atmosphere,
                                 self.hydrographics, self.population,
                                 self.government, self.law_level,
                                 self.tech_level)
        self.trade_classes = self._generate_trade_classes()
        self.bases         = self._generate_bases()
        self.gas_giant     = self._generate_gas_giant()

    def __init__(self):
        self.name          = random.choice(("Erehwemos", "Lacipyt"))
        self.starport      = self._generate_starport()
        self.contents      = self._generate_contents()
        self.size          = self._generate_size()
        self.atmosphere    = self._generate_atmosphere()
        self.hydrographics = self._generate_hydrographics()
        self.population    = self._generate_population()
        self.government    = self._generate_government()
        self.law_level     = self._generate_law_level()
        self.tech_level    = self._generate_tech_level()
        self.uwp           = UWP(self.starport, self.size, self.atmosphere,
                                 self.hydrographics, self.population,
                                 self.government, self.law_level,
                                 self.tech_level)
        self.trade_classes = self._generate_trade_classes()
        self.bases         = self._generate_bases()
        self.gas_giant     = self._generate_gas_giant()

    def __str__(self):
        return "{:16} {} {} {:49} {}".format(
            self.name, 
            self.uwp, 
            self.bases, 
            self.trade_classes, 
            self.gas_giant)

    def _generate_starport(self):
        result = roll(2)
        if result < 5:
            result = 'A'
        elif result < 7:
            result = 'B'
        elif result < 9:
            result = 'C'
        elif result == 9:
            result = 'D'
        elif result < 12:
            result = 'E'
        else:
            result = 'X'
        return result

    def _generate_contents(self):
        result = [False, False, False]
        if self.starport in ('A', 'B'):
            result[0] = roll(2) > 7
        if self.starport not in ('E', 'X'):
            r = roll(2)
            if self.starport == 'C':
                r -= 1
            elif self.starport == 'B':
                r -= 2
            elif self.starport == 'A':
                r -= 3
            result[1] = r > 6
        result[2] = roll(2) < 10
        return result

    def _generate_bases(self):
        result = ' '
        if self.contents[0]:
            if self.contents[1]:
                result = 'A'
            else:
                result = 'N'
        elif self.contents[1]:
            result = 'S'
        return result

    def _generate_gas_giant(self):
        if self.contents[2]:
            return 'G'
        return ' '

    def _generate_size(self):
        return roll(2) - 2

    def _generate_atmosphere(self):
        result = roll(2) - 7 + self.size
        if self.size == 0:
            return 0
        return max(0, min(result, 12))

    def _generate_hydrographics(self):
        if self.size in (0, 1):
            return 0
        result = roll(2) + self.size
        if self.atmosphere < 2 or self.atmosphere > 9:
            result -= 4
        return max(0, min(result, 10))

    def _generate_population(self):
        return roll(2) - 2

    def _generate_government(self):
        return max(0, min(14, roll(2) - 7 + self.population))

    def _generate_law_level(self):
        return max(0, min(10, roll(2) - 7 + self.government))

    def _generate_tech_level(self):
        elements = (str(self.starport), str(self.size), str(self.atmosphere),
                    str(self.hydrographics), str(self.population),
                   str(self.government))
        modifiers = []
        result = roll()
        with open('tech_level.csv') as file:
            tl = csv.DictReader(file, dialect='excel')
            for row in tl:
                modifiers.append(row)
        for i in range(len(elements)): # might be a better way to do this
            result += int(modifiers[i][str(elements[i])])
        return result

    def _generate_trade_classes(self):
        result = []
        if (4 <= self.atmosphere <= 9 and 
            4 <= self.hydrographics <= 8 and
            5 <= self.population <= 7):
            result.append("Agricultural.")
        if (self.atmosphere <= 3 and
            self.hydrographics <= 3 and
            self.population >= 6):
            result.append("Non-Agricultural.")
        if (self.atmosphere in (0, 1, 2, 4, 7 ,9) and 
            self.population >= 9):
            result.append("Industrial.")
        if (self.population <= 6):
            result.append("Non-Industrial.")
        if (self.atmosphere in (6, 8) and
            6 <= self.population <= 8 and
            4 <= self.government <= 9):
            result.append("Rich.")
        if (2 <= self.atmosphere <= 5 and
            self.hydrographics <= 3):
            result.append("Poor.")
        if self.hydrographics == 10:
            result.append("Water World.")
        if (self.hydrographics == 0 and 
            self.atmosphere >= 2):
            result.append("Desert World.")
        if self.atmosphere == 0:
            result.append("Vacuum World.")
        if self.size == 0:
            result.append("Asteroid Belt.")
        if (self.atmosphere < 2 and
            self.hydrographics > 1):
            result.append("Ice-capped.")
        return " ".join(result)


if __name__ == "__main__":
    w = World()
    print(w)
