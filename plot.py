#!/usr/bin/env python
import serial
from time import sleep
import sys

# rawe 10.12.2015
# script to feed an HPGL file from Inkscape or somewhere on the web via UART to an Roland DXY-990
# tested so far:
# - attached Chaosknoten
# - Autodesk Spaceshutle Columbia
#
# TODO: - make commandline argument handling nicer, wrap code in some function etc.


infile = file(sys.argv[1])

intext = infile.read()
infile.close()
intext = intext.replace("\n",";") # in some HPGL files found there are newlines only, but no ";". Add these to make splitting commands easy.
cmds = intext.split(";")

# pre processor: split multi-point PD into single PDs. Inkscape likes to create these but Roland DXY-990 does not understand these.
outcmds = []

for item in cmds:
   if "PD" in item and "," in item and len(item.split(","))>2:
      #print "multipd!"
      xy = False
      singlepoints = item[2:].split(",")
      x = 0
      for point in singlepoints:

         if xy == False:
            x = point
         else:
            outcmds.append("PD"+str(x)+","+str(point))

         if xy == False:
            xy = True
         else:
            xy = False
   else:
      outcmds.append(item)

cmds = outcmds


# scaling added, as hpgl files from the web seem to be way too big or way too small
scale = float(sys.argv[2])


if not sys.argv[3] == "sim":
   # serial port is opened with rtscts flow control and other setings. Flow control by rtscts allows us to get away
   # without escape sequences to check for a full buffer (e.g. "\x28.B").
   s = serial.Serial("/dev/ttyUSB0",rtscts=1, baudrate=9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0.01)


for cmd in cmds:
   if "," in cmd: # oh, something to scale
      x,y = cmd[2:].split(",")
      cmd = cmd[:2]+str(int(int(x)*scale))+","+str(int(int(y)*scale))

   cmd+=";" # every command ends with an ;
   print cmd # display on screen
   if not sys.argv[3] == "sim":
      s.write(cmd)

if s:
   s.close()
