#!/usr/bin/python

############################################################################
#    flow2rank.py                                                          #
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

import sys, re

debug = 0

if len(sys.argv) < 2:
    dbg ( "Usage: ", sys.argv[0], " <column to rank by>")
    exit(1)
col = int(sys.argv[1])

def dbg(*args):
    global debug
    if not debug:
        return
    for a in args:
        print >> sys.stderr, a,
    print >> sys.stderr

pairs = {}

for line in sys.stdin:
    if line == '\n' or line[0] == '#':
        continue
    l = re.split('\t', line[:-1])
    src = l[0]
    dst = l[1]
    val = l[col - 1]
    pair = ''
    if src < dst:
        pair = src + ',' + dst
    else:
        pair = dst + ',' + src
    if pairs.has_key(pair):
        pairs[pair] += int(val)
    else:
        pairs[pair] = int(val)

l = list(pairs.items())

l.sort(cmp = lambda x, y: cmp(x[1], y[1]), reverse = True)

for i in l:
    print i[0] + '\t' + str(i[1])
