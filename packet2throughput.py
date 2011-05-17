#!/usr/bin/python

############################################################################
#    packet2throughput.py                                                  #
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
    dbg ( "Usage: ", sys.argv[0], " <seconds>")
    exit(1)
interval = int(sys.argv[1])
start = None
cstart = None
first = True
count = 0
cbytes = 0

def dbg(*args):
    global debug
    if not debug:
        return
    for a in args:
        print >> sys.stderr, a,
    print >> sys.stderr

max = 0;

for line in inp:
    if line == '\n' or line[0] == '#':
        continue
    l = re.split('\t', line[:-1])
    cstart = float(l[0])
    if cstart < max:
        raise Exception("input not sorted! Got ", l[0], ' max ', str(max))
    max = cstart
    if first:
        start = cstart
        first = False
    
    if cstart < start + interval:
        dbg ( "inserting: ", cstart)
        cbytes += int(l[1])
    else:
        # enter next interval
        # clean active flows
        dbg ( "proc: ", start, interval)
        print float(cbytes) / interval
        while cstart > start + 2 * interval:
            dbg ( "mproc: ", start+interval, interval)
            print 0
            start += interval
        dbg ( "edge inserting: ", cstart)
        cbytes = int(l[1])
        start += interval
    
print float(cbytes) / interval