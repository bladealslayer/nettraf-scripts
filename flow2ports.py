#!/usr/bin/python

############################################################################
#    flow2ports.py                                                         #
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

output_packets = True
p2p = False
tcp_udp = True

if len(sys.argv) == 2 and 'a' in sys.argv[1]:
    tcp_udp = False
    
if len(sys.argv) == 2 and 't' in sys.argv[1]:
    p2p = True

def dbg(*args):
    global debug
    if not debug:
        return
    for a in args:
        print >> sys.stderr, a,
    print >> sys.stderr

ports = {}

for line in sys.stdin:
    if line == '\n':
        continue
    l = re.split('\t', line[:-1])
    proto = int(l[2])
    if tcp_udp and proto != 6 and proto != 17:
        # check only TCP and UDP protocols
        continue
    sport = int(l[4])
    dport = int(l[5])
    flows = int(l[8])
    bytes = int(l[7])
    packets = int(l[6])
    if p2p and (sport < 1024 or dport < 1024):
        continue
    for port in [sport, dport]:
        if port < 1 or port > 65535:
            continue
        if ports.has_key(port):
            t = ports[port]
            ports[port] = (t[0] + bytes, t[1] + flows, t[2] + packets)
        else:
            ports[port] = (bytes, flows, packets)

for p, t in ports.items():
    if output_packets:
        print str(p) + '\t' + str(t[0]) + '\t' + str(t[1]) + '\t' + str(t[2])
    else:
        print str(p) + '\t' + str(t[0]) + '\t' + str(t[1])
