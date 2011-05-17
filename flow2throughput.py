#!/usr/bin/python

############################################################################
#    flow2throughput.py                                                    #
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

active = []
if len(sys.argv) < 2:
    dbg ( "Usage: ", sys.argv[0], " <seconds>")
    exit(1)
interval = int(sys.argv[1])
start = None
cstart = None
first = True
count = 0

intervals = []

def insert_active(a, v):
    a.append(v)

def dbg(*args):
    global debug
    if not debug:
        return
    for a in args:
        print >> sys.stderr, a,
    print >> sys.stderr

def process_interval(intervals, a, s, length):
    thr = 0
    bytes = 0
    i = 0
    while i < len(a):
        l = a[i]
        cs = float(l[1])
        ce = float(l[2])
        cbytes = 0.00
        dbg('considering: ', cs, ce)
        if ce == cs:
            cbytes = int(l[0])
            dbg('byes: instant flow: ', cbytes)
        elif cs >= s and ce <= s + length:
            cbytes = int(l[0])
            dbg ('bytes: full: ', cbytes)
        elif cs >= s:
            cbytes = (float(l[0]) / (float(l[2]) - float(l[1]))) * (float(s)+length - cs)
            dbg('bytes: partial starting: ', cbytes)
        elif ce <= s + length:
            cbytes = (float(l[0]) / (float(l[2]) - float(l[1]))) * (ce - s)
            dbg('bytes: partial ending: ', cbytes)
        elif cs < s and ce > s + length:
            cbytes = (float(l[0]) / (float(l[2]) - float(l[1]))) * length
        if bytes < 0:
            raise Exception('Unexpected negative bytes!')
        bytes += cbytes
        if ce < float(s)+length:
            # clean this one
            a.pop(i)
        else:
            i += 1
    thr = bytes / length
    intervals.append(thr)
    print thr
    dbg(thr)

max = 0;

for line in inp:
    if line == '\n' or line[0] == '#':
        continue
    l = re.split('\t', line[:-1])
    cstart = float(l[1])
    if cstart < max:
        raise Exception("input not sorted!")
    max = cstart
    if first:
        start = cstart
        first = False
    
    if cstart < start + interval:
        dbg ( "inserting: ", cstart)
        insert_active(active, l)
    else:
        # enter next interval
        # clean active flows
        dbg ( "proc: ", start, interval)
        process_interval(intervals, active, start, interval)
        while cstart > start + 2 * interval:
            dbg ( "mproc: ", start+interval, interval)
            process_interval(intervals, active, start+interval, interval)
            start += interval
        dbg ( "edge inserting: ", cstart)
        insert_active(active, l)
        start += interval
    
    count += 1
while len(active) > 0:
    dbg('final proc: ' + str(start))
    process_interval(intervals, active, start, interval)
    start += interval

if len(active) > 0:
    dbg ( active)
    raise Exception('Not all flows processed!')
