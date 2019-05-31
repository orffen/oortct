# uwp.py -- Orffen's Referee Toolbox for Classic Traveller
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

from uc import uc

class UWP(object):
    """Creates a Universal World Profile using eHex."""
    def __init__(self, starport, size, atmosphere, hydrographics, population,
                 government, law_level, tech_level):
        self._profile = []
        self._profile.append(uc(starport))
        self._profile.append(uc(size))
        self._profile.append(uc(atmosphere))
        self._profile.append(uc(hydrographics))
        self._profile.append(uc(population))
        self._profile.append(uc(government))
        self._profile.append(uc(law_level))
        self._profile.append("-")
        self._profile.append(uc(tech_level))

    def __str__(self):
        return "".join(self._profile)
