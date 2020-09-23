#!/usr/bin/env python

import subprocess

options = [
           ['Redo_VNA', 'TP_1m_13_ChD3_ChCMD.vna'],
           ['Redo_VNA', 'TP_1m_55_ChD1.vna'],
           ['Redo_VNA', 'straight_SMA.vna'],
	   ]


command = 'python readVNADataSKRF.py --basename={0:s}/{1:s}'

for opt in options:
    s = command.format(
      	opt[0], opt[1]
	)
	
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)

    subprocess.call( [s, ""], shell=True )	

