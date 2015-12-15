#!/usr/bin/env python
import serial
from time import sleep
import sys

# rawe 10.12.2015
# script to feed an HPGL file from Inkscape or somewhere on the web via UART to an Roland DXY-990
# tested so far:
# - attached Chaosknoten
# - Autodesk Spaceshutle Columbia



if not ( len(sys.argv) == 5 or len(sys.argv) == 6):
   print "this.py input-file scale offsetx offsety plotter-device"
   print "this.py drawing.hpgl 3.5 1000 1000 /dev/ttyUSB0"
   quit()


infile = file(sys.argv[1])
scale = float(sys.argv[2])
offset = float(sys.argv[3]),float(sys.argv[4])

plotdev = False
if len(sys.argv) == 6:
   plotdev = sys.argv[5]


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



extreme_coordinates = [False, False, False, False]



if plotdev:
   # serial port is opened with rtscts flow control and other setings. Flow control by rtscts allows us to get away
   # without escape sequences to check for a full buffer (e.g. "\x28.B").
   s = serial.Serial(plotdev,rtscts=1, baudrate=9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0.01)


for cmd in cmds:
   if "," in cmd: # oh, something to scale
      x,y = cmd[2:].split(",")
      x,y = int(int(x)*scale+offset[0]),int(int(y)*scale+offset[1])
      cmd = cmd[:2]+str(x)+","+str(y)

      if extreme_coordinates[0] == False or x < extreme_coordinates[0]:
         extreme_coordinates[0] = x
      if extreme_coordinates[1] == False or y < extreme_coordinates[1]:
         extreme_coordinates[1] = y
      if extreme_coordinates[2] == False or x > extreme_coordinates[2]:
         extreme_coordinates[2] = x
      if extreme_coordinates[3] == False or y > extreme_coordinates[3]:
         extreme_coordinates[3] = y




   cmd+=";" # every command ends with an ;
   print cmd # display on screen
   if plotdev:
      s.write(cmd)

print "extreme coordinates (x/y in mm) [%f,%f ; %f,%f ] = size (w/h in mm) [%f,%f]"%(extreme_coordinates[0]/40.0, extreme_coordinates[1]/40.0, extreme_coordinates[2]/40.0, extreme_coordinates[3]/40.0, (extreme_coordinates[2]-extreme_coordinates[0])/40.0, (extreme_coordinates[3]-extreme_coordinates[1])/40.0)

if plotdev:
   s.close()
