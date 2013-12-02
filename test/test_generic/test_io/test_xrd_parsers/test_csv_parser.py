#!/usr/bin/python
# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

import unittest

from test.test_generic.test_io.test_file_parsers import TestParserMixin
from pyxrd.generic.io.xrd_parsers import CSVParser


__all__ = [
    'TestCSVParser',
]

class TestCSVParser(TestParserMixin, unittest.TestCase):

    parser_class = CSVParser
    file_data = [
        r""""2θ" "Total" "Illite" "Kaolinite" "Kaolinite HCSDS" "ISS R0 GLY" "KSS R0 Ca-GLY" "KSSS R0 Ca-GLY"
3.02755700 273.16049233 97.02814022 31.38556697 35.59578617 23.51568141 48.65379108 94.57724147
3.04755700 270.13870087 95.62476636 31.06940638 35.22982402 23.36216182 48.62501123 93.82324607
3.06755700 267.22786165 94.28393668 30.76061580 34.87300927 23.21212148 48.60496947 93.08892395
3.08755700 264.42041889 93.00398290 30.45939344 34.51998503 23.06538817 48.59361044 92.37377390
3.10755700 261.70360562 91.77676261 30.16586741 34.16672250 22.92177298 48.59088431 91.67731080
3.12755700 259.06212412 90.58942248 29.88008630 33.81143245 22.78108632 48.59674661 90.99906497
3.14755700 256.48113103 89.42706605 29.60201371 33.45487360 22.64315301 48.61115803 90.33858163
3.16755700 253.94889023 88.27574451 29.33152685 33.10000476 22.50782446 48.63408424 89.69542041
3.18755700 251.45858095 87.12514462 29.06841908 32.75109518 22.37498655 48.66549574 89.06915477
3.20755700 249.00896711 85.97043387 28.81240611 32.41254039 22.24456254 48.70536766 88.45937154
3.22755700 246.60389183 84.81291555 28.56313541 32.08769488 22.11651102 48.75367958 87.86567038
3.24755700 244.25080155 83.65940329 28.32019837 31.77801661 21.99081961 48.81041538 87.28766329
3.26755700 241.95867992 82.52049022 28.08314451 31.48272743 21.86749559 48.87556303 86.72497414
3.28755700 239.73585293 81.40810814 27.85149708 31.19905514 21.74655494 48.94911440 86.17723824
3.30755700 237.58810884 80.33290306 27.62476936 30.92297304 21.62801143 49.03106510 85.64410184""",
        r""""2θ","Total","Illite","Kaolinite","Kaolinite,HCSDS","ISS,R0,GLY","KSS,R0,Ca-GLY","KSSS,R0,Ca-GLY"
3.02755700,273.16049233,97.02814022,31.38556697,35.59578617,23.51568141,48.65379108,94.57724147
3.04755700,270.13870087,95.62476636,31.06940638,35.22982402,23.36216182,48.62501123,93.82324607
3.06755700,267.22786165,94.28393668,30.76061580,34.87300927,23.21212148,48.60496947,93.08892395
3.08755700,264.42041889,93.00398290,30.45939344,34.51998503,23.06538817,48.59361044,92.37377390
3.10755700,261.70360562,91.77676261,30.16586741,34.16672250,22.92177298,48.59088431,91.67731080
3.12755700,259.06212412,90.58942248,29.88008630,33.81143245,22.78108632,48.59674661,90.99906497
3.14755700,256.48113103,89.42706605,29.60201371,33.45487360,22.64315301,48.61115803,90.33858163
3.16755700,253.94889023,88.27574451,29.33152685,33.10000476,22.50782446,48.63408424,89.69542041
3.18755700,251.45858095,87.12514462,29.06841908,32.75109518,22.37498655,48.66549574,89.06915477
3.20755700,249.00896711,85.97043387,28.81240611,32.41254039,22.24456254,48.70536766,88.45937154
3.22755700,246.60389183,84.81291555,28.56313541,32.08769488,22.11651102,48.75367958,87.86567038
3.24755700,244.25080155,83.65940329,28.32019837,31.77801661,21.99081961,48.81041538,87.28766329
3.26755700,241.95867992,82.52049022,28.08314451,31.48272743,21.86749559,48.87556303,86.72497414
3.28755700,239.73585293,81.40810814,27.85149708,31.19905514,21.74655494,48.94911440,86.17723824
3.30755700,237.58810884,80.33290306,27.62476936,30.92297304,21.62801143,49.03106510,85.64410184""",
    ]

    pass # end of class