#!/usr/bin/python

############################################################################
#    flow2length.py                                                        #
#    v0.1                                                                  #
#                                                                          #
#    Copyright (C) 2011 by Boyan Tabakov                                   #
#    blade@alslayer.net                                                    #
#                                                                          #
#    This program is free software; you can redistribute it and/or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import sys,re

inp = sys.stdin

count = False

if len(sys.argv) > 1 and sys.argv[1] == '-c':
    count = True

total = 0

for line in inp:
    if line == '\n' or line[0] == '#':
        continue
    l = re.split('\t', line[:-1])
    bytes = int(l[7])
    flows = int(l[8])
    if not count:
        for i in xrange(0, flows):
            print float(bytes) / flows
            if bytes == 0:
                print line[:-1]
    else:
        total += flows

if count:
    print total