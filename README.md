# penplotterfeeder
feeds hpgl files from inkscape via usb-rs232 adapter to my roland DXY-990 pen plotter. Includes scaling/offset addition and "fixes" HPGL so the plotter understands it. By no way this is a complete HPGL-conform interpreter, it understands the HPGL subset Inkscape exports and converts it to something my plotter understands.

Plotter switch settings:
SW-1: 0000 (charset), 1 (serial), 0 (reserved), 11 (A4; 10 = A3), 00 (reserved)

SW-2: 100 (baud 9600), 0 (D), 1 (EN), 1 (even parity), 1 (7 data bits), 0 (1 stopbit)

Known Bugs:
After the script finishes the plotter stops after some time as the RS232 control lines may get modified by another process or the usb uart driver itself. A simple work-around is to add a waiting time to make sure the plotter finishes. A better way would be a function to ask the plotter for its buffer level and exit after the buffer is empty.

You may want to have a look at https://pypi.python.org/pypi/Chiplotle . It seems to be a great API/library, but I found it "over-engineered" for the simple task of piping data to a plotter.
