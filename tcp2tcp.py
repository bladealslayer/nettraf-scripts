#!/usr/bin/python

############################################################################
#    tcp2tcp.py                                                            #
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

debug = 0

if len(sys.argv) < 2:
    dbg ( "Usage: ", sys.argv[0], " <frame file>")
    exit(1)

def dbg(*args):
    global debug
    if not debug:
        return
    for a in args:
        print >> sys.stderr, a,
    print >> sys.stderr

frames = []
f_index = 0

fr = open(sys.argv[1], 'r')

first_line = True

for line in inp:
    if line == '\n' or line[0] == '#':
        continue
    if first_line:
        first_line = False
        print line[:-1] + '\tcurrent_throughput'
        continue
    l = re.split('\t', line[:-1])
    cstart = float(l[8])
    cend = float(l[9])
    if cend <= cstart:
        continue
        raise Exception('bad connection times')
    cbytes = 0
    fr.seek(f_index)
    seeking = True
    for f in fr:
        ll = len(f)
        f = re.split('\t', f[:-1])
        ts = float(f[0])
        if ts < cstart:
            f_index += ll
            seeking = False
            continue
        if ts > cend:
            break
        cbytes += int(f[1])
    
    thr = float(cbytes) / (cend - cstart)
    print line[:-1] + '\t' + str(thr)