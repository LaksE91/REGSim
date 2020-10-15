###########################################################################
### Estimation of lateral flow using Darcy's equation                   ###
### Author : Lakshmi E                                                  ###
### Last Edit: 13-April-2020                                            ###
###########################################################################

import arcpy,csv,os
from arcpy import env
from arcpy.sa import *
import numpy as np

arcpy.env.OverwriteOutput=True

#set the currect directory
env.workspace=(input("give the current directory:"))#'C:\Users\Laks\Desktop\REGSim module'
dirpath = os.getcwd()

# estimate lateral inflow and outflow
data            = open(r'output.csv')
data            = csv.reader(data)
data            = list(data) # reading all data at once

# assign variables
s_in            = []
s_out           = []
Q_in            = []
Q_out           = []

print "\niterating using zip"
for i in data:
    f           = i[0]+ '.shp'
    shapearea   = []
    fc1         = f      
    searchCol   = ["Slope"]
    with arcpy.da.SearchCursor(fc1,searchCol) as sc:
        for row in sc:
            s   = float(row[0])
            shapearea.append(s)
            inf,outf    = [i for i in shapearea if i<0 ],[j for j in shapearea if j>0]
        temp_in         = np.mean(inf)
        temp_out        = np.mean(outf)
    s_in.append(temp_in*-1)
    s_out.append(temp_out*1)

# estimate net lateral flow
trans           = input('Transmissivity of the aquifer:(unit m2/day)')  #m2/day 
shpfile         = input('Polyline study area boundary shapefile:')#'bound_hmda_line.shp'

length          = arcpy.da.SearchCursor(shpfile,'Length').next()[0]
const           = (length * trans)/0.033    # converting day to month ---> 0.003

print "\niterating using zip"
# Darcy flow --> Q = T*i*l
for (jj,kk) in zip(s_in,s_out):
    Q_in.append(jj*const)
    Q_out.append(kk*const)

print Q_in,Q_out

#write the flow data in txt format
infile      = open(r'Q_in.txt', 'w')
outfile     = open(r'Q_out.txt','w')

for (i,j) in zip(Q_in,Q_out):
  infile.write("%f10\n" % i)
  outfile.write("%f10\n" % j)

print '\n Lateral inflow and outflow are estimated'

# end of the script
